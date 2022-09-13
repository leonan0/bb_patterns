def get_next_range(df, start_index, range, gap):
    nstart = start_index + 1 + gap
    return df.loc[nstart:nstart+range - 1]
