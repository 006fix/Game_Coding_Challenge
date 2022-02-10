#
#
# details of the various hardcoded AI models used:
#
# 1.) Generic Random - copy of the phase 1 AI. Randomly picks from an option it can build:
#     If there is a valid option to build, it will always build
#
# 2.) Field Focus - it a field is available to build, always build a field (random choice). If not, always
# build something regardless
#
# 3.) Field focus - lowest level - if a field is available to build, always build, but prioritise the lowest level:
#     If not available, choose the lowest level building
#
# 4.) Field focus - weighting preference. Similar concept to 2.), but with variable weightings for all field types,
# and buildings
#
# 5.) Field focus - weighting preference, lowest level. Similar to 4.), but using the lowest level priorities from 3
# but only for fields
#
# 6.) Main building - preferentially prioritises the main building in all instances, otherwise random
#
# 7.) Early field focus - prioritises fields till every field is level 5, then main building focus till 10, then random
#
# 8.) Early field focus - weightings - same as 7.) but with variable focus weightings
#
# 9.) Full genetic weighting - complete set of weightings for all building types and levels
#
# 10.) Level by level. Levels all buildings and fields in sequence, one after the other
#
# 11.) Level by level mod. Till fields at 6, level fields twice for every level of buildings, then one by one
#
# Logic:
#     Genetic algorithms will be used for 4, 5, 8, 9
#
# For all cases where genetic algorithms are used, they will be trained for a number of generations
# Once trained, they can be incorporated into the remainder
#
# In all instances, 4 types of outcomes will be considered:
#     Pop score
#     CP score
#     Res score
#     Combined score
#
# For combined score, res, cp, and pop will all be normalised to a range of 0-1, then used as a metric
#
