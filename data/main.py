# EXTERNAL ITEMS
import pandas as pd
    # for data processing
import sys
    # for filepath arguments
import sc2reader
    # the replay file reader module
from sc2reader.engine.plugins import APMTracker, SelectionTracker

# GLOBALS
__myNone = 'NA'
    # This will represent a missing value from replay data
        # in a dictionary.

# CODE

def get_dictVal_OR_myNone(nestedDict, accessChain):
    """
    :param accessChain: an access list, e.g. dict[accessChain[0]][accessChain[1]]...
    :return: corresponding dict value or __myNone
    """

    val = nestedDict
        # if len(accessChain) == 0, return nestedDict

    # traverse layers of dict until accessChain finds value
        # or the access chain is found to be invalid
    for s in accessChain:

        if not(isinstance(val, (dict, list))) and ('__dict__' in dir(val)):
            val = vars(val)

        if not(isinstance(val, (dict, list))) or not(s in val) or (val[s] is None):
            return __myNone
        else:
            val = val[s]

    # return found & valid value
    return val

def collect_units( replay ):
    """
    :param replay: the replay object
    :return: units: the replay object with only the desired attributes
    """

    """
    The documentation at https://pandas-docs.github.io/pandas-docs-travis/generated/pandas.DataFrame.from_dict.html
    >>> data = {'row_1': [3, 2, 1, 0], 'row_2': ['a', 'b', 'c', 'd']}
    >>> pd.DataFrame.from_dict(data, orient='index')
           0  1  2  3
    row_1  3  2  1  0
    row_2  a  b  c  d
    
    When using the ‘index’ orientation, the column names can be specified manually:
    
    >>> pd.DataFrame.from_dict(data, orient='index',
    ...                        columns=['A', 'B', 'C', 'D'])
           A  B  C  D
    row_1  3  2  1  0
    row_2  a  b  c  d
    """

    all_units = {}
        # collect all units here

    # helper function
    # IMPORTANT this determines which attributes are considered 'desired'
    def transfer_desired_attributes(unitVars_from, unitVars_to):
        # identification info
        unitVars_to['id'] = get_dictVal_OR_myNone(#unitVars_from.id
            unitVars_from,
            ['id']
        )
        # owner info
        unitVars_to['owner_name'] = get_dictVal_OR_myNone(#unitVars_from.owner.detail_data['name']
            unitVars_from,
            ['owner', 'detail_data', 'name']
        )
        unitVars_to['owner_is_human'] = get_dictVal_OR_myNone(#unitVars_from.owner.is_human
            unitVars_from,
            ['owner', 'is_human']
        )
        # booleans
        unitVars_to['is_army'] = get_dictVal_OR_myNone(#unitVars_from.is_army
            unitVars_from,
            ['is_army']
        )
        unitVars_to['is_building'] = get_dictVal_OR_myNone(#unitVars_from.is_building
            unitVars_from,
            ['is_building']
        )
        unitVars_to['is_worker'] = get_dictVal_OR_myNone(#unitVars_from.is_worker
            unitVars_from,
            ['is_worker']
        )
        # lifespan info
        unitVars_to['started_at'] = get_dictVal_OR_myNone(#unitVars_from.started_at
            unitVars_from,
            ['started_at']
        )
        unitVars_to['finished_at'] = get_dictVal_OR_myNone(#unitVars_from.finished_at
            unitVars_from,
            ['finished_at']
        )
        unitVars_to['died_at'] = get_dictVal_OR_myNone(#unitVars_from.died_at
            unitVars_from,
            ['died_at']
        )
        return

    # collect all units from all players
    for player in replay.players:

        # collect units from player.units
        for u in player.units:

            temp_unit = {}
                # to hold one simplified unit from player.units
            transfer_desired_attributes(vars(u), temp_unit)
                # transfer desired attributes from u to temp_unit
            temp_intergame_id = temp_unit['owner_name'] + str(temp_unit['id'])
                # key for temp_unit
                # cannot simply be id since id is unique to
                    # a single game
            all_units[ temp_intergame_id ] = temp_unit
                # add to all_units using key

        # collect units from player.killed_units
        for u in player.killed_units:

            temp_unit = {}
            transfer_desired_attributes(vars(u), temp_unit)
            temp_intergame_id = temp_unit['owner_name'] + str(temp_unit['id'])

            # only add unit from killed_units if it wasn't in units
            if temp_intergame_id in all_units:
                continue
            else:
                all_units[ temp_intergame_id ] = temp_unit

    return all_units


def replayObj_to_csv( replay, csvFilepath ):

    # collect all units in the replay
    units = collect_units(replay)

    # move replay object to dataframe, a table-like structure
    unitsDf = pd.DataFrame.from_dict(
        data=units,
            # take data from units
        orient='index',
            # orient to rows
            # each element element (nested dictionary) in units will be a row.
            # iow, each key in units represents a row.
        dtype=None
            # do not coerce data types
    )

    # export dataframe to csv file
    unitsDf.to_csv(
        path_or_buf = csvFilepath,
            # destination filepath
        sep=',',
            # delimiter
        na_rep=__myNone,
            # 'NA' will represent missing data
        float_format=None,
            # no need to truncate/format floating-point numbers
        header=True,
            # write out column names
        index=True,
            # write row names (indices)
        line_terminator='\n'
    )
    return

def main():
    filepath = sys.argv[1]
        # command line argument
    replay = sc2reader.load_replay(filepath, load_level=4)
        # save replay object
    replayObj_to_csv(replay, 'csvTest.csv')
        # do everything we want to do to replay
    return

# if client wants to use this file as a library,
    # do not execute.
# else if client wants to execute...
if __name__ == '__main__':
    main()