import pandas as pd

from models.bto_enums import EthnicType, BlockType

if __name__ == "__main__":
    df: pd.DataFrame = pd.read_csv("all_unit_information.csv")

    """
    save multiple dataframes to a single excel, each dataframe under one sheet
    """
    writer = pd.ExcelWriter("all_unit_information.xlsx", engine="xlsxwriter")

    # print(df[(df['ethnic_type'] == EthnicType.chinese.value) & (df['block_type'] == BlockType.blk_132a.value)])

    for ethnic_type in EthnicType:
        for block_type in BlockType:
            curr_df = df[(df['ethnic_type'] == ethnic_type.value) & (df['block_type'] == block_type.value)]
            curr_df.to_excel(writer, f"{ethnic_type.replace('/', ' or ')}_{block_type}", columns=curr_df.columns, index=False)

    writer.save()

