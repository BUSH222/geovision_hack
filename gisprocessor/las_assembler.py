import lasio


def las_assembler(graph_text, well_info, digitised_data):
    # Create an empty LAS file
    well = lasio.LASFile()

    # Add depth info
    graph_number, curve_data = list(graph_text.items())[0]
    print(digitised_data[graph_number])
    mnem, unit, description = curve_data
    data = [k[0] for k in digitised_data[graph_number]]
    well.insert_curve(0, 'DEPTH', data, '.M', 'Depth')

    # Populate curve information section (graph_text)
    for graph_number, curve_data in graph_text.items():
        mnem, unit, description = curve_data
        data = [k[1] for k in digitised_data[graph_number]]
        well.insert_curve(graph_number+1, mnem, data, unit, description)

    # Populate well information section
    for item in well_info:
        mnem, unit, data_type, info = item
        well.params[mnem] = lasio.HeaderItem(unit=unit, value=data_type, descr=info)

    return well


if __name__ == '__main__':
    graph_text = {1: ['PZ', '.Ohmm', 'POTENTIAL RESISTIVITY BORE'], 2: ['MPZ', '.Ohmm', 'MICRO POTENTIAL LOG BORE']}
    well_info = [['STRT', '.M', 3088.0000, 'Start depth'], ['STOP', '.M', 3088.2000, 'Stop depth'],
                 ['STEP', '.M', 0.1000, 'Step'], ['NULL', '.', -9999, 'Null value']]
    digitised_data = {1: [[3088.0000, 5], [3088.1000, 2], [3088.2000, 3]],
                      2: [[3088.0000, 6], [3088.1000, 6], [3088.2000, 9]]}
    las_assembler(graph_text, well_info, digitised_data)
