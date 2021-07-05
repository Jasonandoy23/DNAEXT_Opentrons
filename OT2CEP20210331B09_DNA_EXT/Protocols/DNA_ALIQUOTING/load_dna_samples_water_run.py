######################################################################
######### DNA ALIQUOTING FOR 2 CRYO VIAL TUBE PLATES #################
######################################################################
from opentrons import protocol_api
import pandas as pd
import numpy as np
import os

# metadata
metadata = {
    'protocolName': 'QC METHOD',
    'author': 'Name <jason.andoy@g42.ai>',
    'description': 'DNA ALIQUOTING for Opentrons',
    'apiLevel': '2.10'
}
water_run = True
positions = ['A1','A2','A3']
DNA_volume = 200.0

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    #### TIP RACKS
    tip_rack1_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', '1')

    #### PLATES

    dna_source_plate = protocol.load_labware('thermofisher_reservoir', '5')
    dna_plate = protocol.load_labware('nest_96_wellplate_2ml_deep_on_chemagic_stand', '2')

    #### PIPETTES
    right_pipette = protocol.load_instrument(
        'p300_multi_gen2', mount='right', tip_racks=[tip_rack1_300ul])

    def load_dna():
        i = 0
        for j in range(len(positions)):
            comment = 'COLUMN NO: ' + str(i+1)
            protocol.comment(comment)
            right_pipette.pick_up_tip()
            # 1ST ALIQUOT
            right_pipette.aspirate(volume=DNA_volume,
                                   location=dna_source_plate['A1'].bottom(2),
                                   rate=0.3)
            right_pipette.air_gap(2)
            protocol.delay(seconds=1)

            right_pipette.dispense(volume=DNA_volume,
                                   location=dna_plate[positions[i]].bottom(4),
                                   rate=0.3)
            right_pipette.blow_out(location=dna_plate[positions[i]].bottom(9))
            protocol.delay(seconds=1)

            # 2nd ALIQUOT
            right_pipette.aspirate(volume=DNA_volume,
                                   location=dna_source_plate['A1'].bottom(2),
                                   rate=0.3)
            right_pipette.air_gap(2)
            protocol.delay(seconds=1)

            right_pipette.dispense(volume=DNA_volume,
                                   location=dna_plate[positions[i]].bottom(4),
                                   rate=0.3)
            right_pipette.blow_out(location=dna_plate[positions[i]].bottom(9))
            protocol.delay(seconds=1)


            if water_run:
                right_pipette.return_tip(home_after=False)
            else:
                right_pipette.drop_tip(home_after=False)
            i = i + 1

    ### COMMANDS ####

    protocol.set_rail_lights(True)
    load_dna()
    protocol.set_rail_lights(False)
