######################################################################
######### DNA ALIQUOTING FOR 2 CRYO VIAL TUBE PLATES #################
######################################################################
from opentrons import protocol_api
import pandas as pd
import numpy as np
import os

# metadata
metadata = {
    'protocolName': 'DNA ALIQUOTING',
    'author': 'Name <jason.andoy@g42.ai>',
    'description': 'DNA ALIQUOTING for Opentrons',
    'apiLevel': '2.10'
}
water_run = True
Source_position = []
Target_position = []
positions = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
# positions = ['A1','A2','A3']
mm_volume = 200.0
DNA_volume = 100.0

file_input_ot2 = '/data/user_files/input.csv'
file_input_local = 'C:/Users/omicstemp/Documents/Opentrons/protocols/Normalization_G42_V1/48input.csv'

df = pd.read_csv(file_input_ot2)

for i in range(len(df)):
    Source_position.append(df['Source'][i])
    Target_position.append(df['Target'][i])

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):
    #### DEFINE LABWARE
    #### TIP RACKS
    tip_rack1_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', '7')

    #### PLATES
    mm_source = protocol.load_labware('thermofisher_reservoir', '5')
    cryo_vial_tubes_1 = protocol.load_labware('nunc_cryo_vial_tubes', '2')
    nunc_target_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', '6')

    #### PIPETTES
    right_pipette = protocol.load_instrument(
        'p300_multi_gen2', mount='right', tip_racks=[tip_rack1_300ul])

    def master_mix_aliquot():
        protocol.comment('MASTER MIX ALIQUOT')
        g = 0
        # right_pipette.pick_up_tip()
        # right_pipette.aspirate(5, mm_source['A1'].bottom(2), rate=0.4)
        for f in range(int(len(Source_position)/8)):
            right_pipette.pick_up_tip()
            right_pipette.aspirate(mm_volume, mm_source['A1'].bottom(2), rate=0.4)
            right_pipette.move_to(mm_source['A1'].top(-2))
            right_pipette.move_to(mm_source['A1'].bottom(2))
            right_pipette.dispense(mm_volume, cryo_vial_tubes_1[Target_position[g]], rate=2.0)

            right_pipette.mix(repetitions=15,
                              volume=DNA_volume,
                              location=cryo_vial_tubes_1[Target_position[g]].bottom(2),
                              rate=10.0)
            right_pipette.aspirate(volume=DNA_volume,
                                   location=cryo_vial_tubes_1[Target_position[g]].bottom(2),
                                   rate=0.3)
            protocol.delay(seconds=2)
            right_pipette.touch_tip()
            right_pipette.air_gap(2)

            right_pipette.dispense(volume=DNA_volume,
                                   location=nunc_target_plate[Target_position[g]].bottom(2),
                                   rate=0.3)
            right_pipette.blow_out(location=nunc_target_plate[Target_position[g]].bottom(1))
            protocol.delay(seconds=1)

            if water_run:
                right_pipette.return_tip(home_after=False)
            else:
                right_pipette.drop_tip(home_after=False)

            g = g + 8

        # right_pipette.dispense(5, mm_source['A1'].bottom(2), rate=0.4)
        # right_pipette.aspirate(5, mm_source['A1'].top(), rate=5.0)

        # if water_run:
        #     right_pipette.return_tip(home_after=False)
        # else:
        #     right_pipette.drop_tip(home_after=False)

    def dna_aliquot():
        i = 0
        for j in range(len(positions)):
            comment = 'COLUMN NO: ' + str(i+1)
            protocol.comment(comment)
            # right_pipette.pick_up_tip()
            # 1ST ALIQUOT
            right_pipette.mix(repetitions=15,
                              volume=DNA_volume,
                              location=cryo_vial_tubes_1[Target_position[i]].bottom(2),
                              rate=10.0)
            right_pipette.aspirate(volume=DNA_volume,
                                   location=cryo_vial_tubes_1[positions[i]].bottom(2),
                                   rate=0.3)
            protocol.delay(seconds=2)
            right_pipette.touch_tip()
            right_pipette.air_gap(2)

            right_pipette.dispense(volume=DNA_volume,
                                   location=nunc_target_plate[positions[i]].bottom(2),
                                   rate=0.3)
            right_pipette.blow_out(location=nunc_target_plate[positions[i]].bottom(1))
            protocol.delay(seconds=1)

            if water_run:
                right_pipette.return_tip(home_after=False)
            else:
                right_pipette.drop_tip(home_after=False)
            i = i + 1


    def flashing_lights():
        for i in range(5):
            protocol.set_rail_lights(True)
            protocol.delay(seconds=0.5)
            protocol.set_rail_lights(False)
            protocol.delay(seconds=0.5)

    ### COMMANDS ####
    protocol.set_rail_lights(True)
    master_mix_aliquot()
    # dna_aliquot()
    flashing_lights()
    protocol.set_rail_lights(True)
