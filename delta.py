import pandas as pd;
import numpy as np

def findDelta(data_frame, delta_to_include=0):
    # delta_to_include can be of these three values:
    #  0 means all differences are included.
    #  1 means only zero or positive differences are included.
    # -1 means only zero or negative differences are included.
    columns_for_delta_calculation = ["icu_patients", "icu_patients_per_million", "hosp_patients_per_million"]
    unique_countries = data_frame["iso_code"].unique()
    delta_df = pd.DataFrame(columns=["iso_code", "date"] + columns_for_delta_calculation + ["new_" + column for column in columns_for_delta_calculation])
    for country in unique_countries:
        filtered_df = data_frame.loc[data_frame["iso_code"] == country, ["iso_code", "date"] + columns_for_delta_calculation]
        for column in columns_for_delta_calculation:
            filtered_df["new_" + column] = np.ediff1d(filtered_df[column], to_begin=0)
            if delta_to_include > 0:
                filtered_df["new_" + column] = filtered_df.apply(lambda x: x["new_" + column] if x["new_" + column] > 0 else 0, axis = 1)
            elif delta_to_include < 0:
                filtered_df["new_" + column] = filtered_df.apply(lambda x: x["new_" + column] if x["new_" + column] < 0 else 0, axis = 1)
        delta_df = pd.concat([delta_df, filtered_df], ignore_index=True)
    return delta_df
