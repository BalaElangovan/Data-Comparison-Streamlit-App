
import streamlit as st
import pandas as pd
from io import BytesIO
import random

# Color Coding
def highlight_diff(df: pd.DataFrame) -> pd.DataFrame:
    css = pd.DataFrame("", index=df.index, columns=df.columns)
    old_row = df.loc["OLD"]
    new_row = df.loc["NEW"]

    for col in df.columns:
        if (pd.isna(old_row[col]) and pd.isna(new_row[col])) or old_row[col] == new_row[col]:
            continue                        # identical → leave blank
        css.loc["OLD", col] = "color: red"   
        css.loc["NEW", col] = "color: yellow"   
    return css

st.title("ELFT Tester")

def load_dataframe(uploaded_file):
    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()          
    buffer = BytesIO(data)

    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(buffer)         
    elif name.endswith(".csv"):
        try:
            return pd.read_csv(buffer)       
        except UnicodeDecodeError:
            buffer.seek(0)
            return pd.read_csv(buffer, encoding="latin1")
    else:
        st.error(f"Unsupported file type: {name}")
        st.stop()

col1, col2 = st.columns(2)
with col1:
    old_file = st.file_uploader(
        "Upload OLD dataset",
        type=["xlsx", "xls", "csv"],
        key="old"
    )
with col2:
    new_file = st.file_uploader(
        "Upload NEW dataset",
        type=["xlsx", "xls", "csv"],
        key="new"
    )

if old_file and new_file:
    old_df = load_dataframe(old_file)
    new_df = load_dataframe(new_file)

    old_cols, new_cols = set(old_df.columns), set(new_df.columns)
    added, removed, common = new_cols - old_cols, old_cols - new_cols, old_cols & new_cols
    
    preferred_exact = ["NHSNumber", "ClientID", "RioID", "ReferralKey"]

#   Fuzzy matches that contain “id” or “key” (case-insensitive)
    preferred_fuzzy = [col for col in common
    if any(tok in col.lower() for tok in ["id", "key"])]

#   Build candidate list: exact hits first, then fuzzy ones, no duplicates
    candidate_keys = [c for c in preferred_exact if c in common] + [c for c in preferred_fuzzy if c not in preferred_exact]

#   Pick the first candidate if any; otherwise fall back to first item
    common_sorted = sorted(common)
    default_key   = candidate_keys[0] if candidate_keys else common_sorted[0]
    default_idx   = common_sorted.index(default_key)

#   Dropdown with autopick
    key_col = st.selectbox(
    "Select key column present in both files:",
    common_sorted,
    index=default_idx,)          # autopick happens here

    with st.expander("Column changes"):
        st.write("**Added in Beta Dashboard:**", added or "None")
        st.write("**Removed from old Dashboard:**", removed or "None")

    if not common:
        st.warning("No common columns found.")
        st.stop()
        
    #  Build the set of IDs present in BOTH files 
    ids_old  = set(old_df[key_col].dropna().astype(str))
    ids_new  = set(new_df[key_col].dropna().astype(str))
    common_ids = sorted(ids_old & ids_new)

    if not common_ids:
        st.warning(f"No matching values for **{key_col}** found in both files.")
        st.stop()

# Randomly pick up to four IDs 
    sample_ids = random.sample(common_ids, k=min(6, len(common_ids)))   # How many columns to check
    st.success(f" Random sample for **{key_col}** → {', '.join(sample_ids)}")

# Compare each sampled ID 
    all_diffs = []       # to collect everything for optional export

    for sid in sample_ids:
        old_row = old_df[old_df[key_col].astype(str) == sid]
        new_row = new_df[new_df[key_col].astype(str) == sid]

        # Should always be true, but sanity-check:
        if old_row.empty or new_row.empty:
            continue

        old_row, new_row = old_row.iloc[0], new_row.iloc[0]

        # Show the two rows (stacked view)
        combo = pd.concat(
            [
                old_row.to_frame().T.assign(Source="OLD"),
                new_row.to_frame().T.assign(Source="NEW")
            ],
            axis=0
        ).set_index("Source")
        
        # Get the color coded change
        combo_style = combo.style.apply(highlight_diff, axis=None)
        st.write(combo_style)

        # Calculate & show diffs
        diffs = [
            (sid, col, old_row[col], new_row[col])
            for col in common
            if not (pd.isna(old_row[col]) and pd.isna(new_row[col]))
            and old_row[col] != new_row[col]
        ]
        if diffs:
            diff_df = pd.DataFrame(
                diffs, columns=[key_col, "Column", "Old Value", "New Value"]
            )
            st.dataframe(diff_df, use_container_width=True)
            all_diffs.append(diff_df)
        else:
            st.info("No differences for this ID.")

# Offer one Excel download for ALL diffs (optional)
    if all_diffs:
        final_df = pd.concat(all_diffs, axis=0, ignore_index=True)
        buf = BytesIO()
        final_df.to_excel(buf, index=False)
        st.download_button(
            "📤 Download ALL diffs (Excel)",
            data=buf.getvalue(),
            file_name=f"comparison_diffs_{key_col}.xlsx",
        )

#   key_col = st.selectbox("Select key column present in both files:", sorted(common))
    key_value = st.text_input(f"Enter the value of '{key_col}' to compare:")

    if key_value:
        old_row = old_df[old_df[key_col].astype(str) == key_value]
        new_row = new_df[new_df[key_col].astype(str) == key_value]
        
#        st.markdown("#### OLD dataset row")  # <-- To change
 #       st.dataframe(old_row, use_container_width=True)

 #       st.markdown("#### NEW dataset row")
 #       st.dataframe(new_row, use_container_width=True)

        combined_df = pd.concat(
            [old_row.assign(Source="OLD"), new_row.assign(Source="NEW")],
            axis=0
        ).set_index("Source")

        st.markdown("#### OLD vs NEW (stacked)")
        st.dataframe(combined_df, use_container_width=True)

        if old_row.empty or new_row.empty:
            st.error(f"ID '{key_value}' not found in both files.")
        else:
            old_row, new_row = old_row.iloc[0], new_row.iloc[0]
            diffs = [
                (col, old_row[col], new_row[col])
                for col in common
                if not (pd.isna(old_row[col]) and pd.isna(new_row[col]))
                   and old_row[col] != new_row[col]
            ]
    

            if diffs:
                diff_df = pd.DataFrame(diffs, columns=["Column", "Old Value", "New Value"])
                st.dataframe(diff_df, use_container_width=True)

                buf = BytesIO()
                diff_df.to_excel(buf, index=False)
                st.download_button(
                    "📤 Download Excel result",
                    data=buf.getvalue(),
                    file_name=f"comparison_result_{key_value}.xlsx"
                )
            else:
                st.success("No differences found for this ID.")
