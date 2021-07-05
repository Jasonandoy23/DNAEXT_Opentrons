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
water_run = False
positions = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
# positions = ['A1','A2','A3']
DNA_volume = 200.0

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):
    #### DEFINE LABWARE
    #### TIP RACKS
    tip_rack1_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', '1')

    #### PLATES
    dna_source_plate = protocol.load_labware('nest_96_wellplate_2ml_deep_on_chemagic_stand', '2')
    cryo_vial_tubes_1 = protocol.load_labware('nunc_cryo_vial_tubes', '5')
    cryo_vial_tubes_2 = protocol.load_labware('nunc_cryo_vial_tubes', '8')

    #### PIPETTES
    right_pipette = protocol.load_instrument(
        'p300_multi_gen2', mount='right', tip_racks=[tip_rack1_300ul])

    def dna_aliquot():
        i = 0
        for j in range(len(positions)):
            comment = 'COLUMN NO: ' + str(i+1)
            protocol.comment(comment)
            right_pipette.pick_up_tip()
            # 1ST ALIQUOT
            right_pipette.aspirate(volume=DNA_volume,
                                   location=dna_source_plate[positions[i]].bottom(2),
                                   rate=0.3)
            protocol.delay(seconds=2)
            right_pipette.touch_tip()
            right_pipette.air_gap(2)

            right_pipette.dispense(volume=DNA_volume,
                                   location=cryo_vial_tubes_1[positions[i]].bottom(4),
                                   rate=0.3)
            right_pipette.blow_out(location=cryo_vial_tubes_1[positions[i]].bottom(9))
            protocol.delay(seconds=1)

            # 2ND ALIQUOT
            right_pipette.aspirate(volume=DNA_volume,
                                   location=dna_source_plate[positions[i]].bottom(1.25),
                                   rate=0.3)
            protocol.delay(seconds=2)
            right_pipette.touch_tip()
            right_pipette.air_gap(2)

            right_pipette.dispense(volume=DNA_volume,
                                   location=cryo_vial_tubes_2[positions[i]].bottom(2),
                                   rate=0.3)
            right_pipette.blow_out(location=cryo_vial_tubes_2[positions[i]].bottom(9))
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
    dna_aliquot()
    flashing_lights()
    protocol.set_rail_lights(True)
