from opentrons import protocol_api, types
import pandas as pd
import numpy as np
import os

# metadata
metadata = {
    'protocolName': 'QC METHOD',
    'author': 'Name <jason.andoy@g42.ai>',
    'description': 'QC METHOD for Opentrons',
    'apiLevel': '2.10'
}
water_run = False
Source_position = []
Target_position = []
mm_volume = 199.0
DNA_volume = 1.0

file_input_ot2 = '/data/user_files/input.csv'
file_input_local = 'C:/Users/omicstemp/Documents/Opentrons/protocols/Normalization_G42_V1/48input.csv'

df = pd.read_csv(file_input_ot2)

for i in range(len(df)):
    Source_position.append(df['Source'][i])
    Target_position.append(df['Target'][i])


# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):
    # DECLARE LABWARES/MODULES
    #### TIP RACKS
    tiprack_only_sample_mixing_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', '7')
    tiprack_mastermix_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', '4')
    tiprack_sample_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', '1')

    #### PLATES
    mm_source = protocol.load_labware('thermofisher_reservoir', '5')
    dna_source_plate = protocol.load_labware('nest_96_wellplate_2ml_deep_on_chemagic_stand', '2')
    nunc_target_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', '6')

    #### PIPETTES
    left_pipette = protocol.load_instrument(
        'p20_multi_gen2', mount='left', tip_racks=[tiprack_sample_20ul])
    right_pipette = protocol.load_instrument(
        'p300_multi_gen2', mount='right', tip_racks=[tiprack_only_sample_mixing_300ul, tiprack_mastermix_300ul])

    def only_sample_mixing():
        protocol.comment('ONLY SAMPLE MIXING')
        d = 0
        for j in range(int(len(Source_position) / 8)):
            right_pipette.pick_up_tip()
            right_pipette.mix(repetitions=15,
                              volume=200.0,
                              location=dna_source_plate[Target_position[d]].bottom(2),
                              rate=10.0)
            right_pipette.blow_out(location=dna_source_plate[Target_position[d]].bottom(8))
            right_pipette.touch_tip()
            right_pipette.aspirate(volume=10,
                                   location=dna_source_plate[Target_position[d]].top(),
                                   rate=10.0)
            if water_run:
                right_pipette.return_tip(home_after=False)
            else:
                right_pipette.drop_tip(home_after=False)
            d = d + 8

    def dna_aliquot():
        protocol.comment('DNA ALIQUOT')
        i = 0
        for j in range(int(len(Source_position) / 8)):
            left_pipette.pick_up_tip()
            left_pipette.aspirate(volume=DNA_volume,
                                  location=dna_source_plate[Source_position[i]].bottom(3.5))
            protocol.delay(seconds=1)
            left_pipette.dispense(volume=DNA_volume,
                                  location=nunc_target_plate[Target_position[i]].bottom(0.3),
                                  rate=30.0)
            # POSITION OFFSETS
            bottom_location = nunc_target_plate[Target_position[i]].bottom(0.4)
            right_offset = bottom_location.move(types.Point(x=2, y=0, z=0))
            left_pipette.move_to(location=right_offset)
            left_pipette.blow_out(location=right_offset)
            i = i + 8
            if water_run:
                left_pipette.return_tip(home_after=False)
            else:
                left_pipette.drop_tip(home_after=False)

    def master_mix_aliquot():
        protocol.comment('MASTER MIX ALIQUOT')
        g = 0
        for j in range(int(len(Source_position) / 8)):
            right_pipette.pick_up_tip()
            right_pipette.aspirate(volume=mm_volume,
                                   location=mm_source['A1'].bottom(0.2))
            protocol.delay(seconds=0.5)
            right_pipette.dispense(volume=mm_volume,
                                   location=nunc_target_plate[Target_position[g]].bottom(1),
                                   rate=10.0)
            right_pipette.mix(repetitions=6,
                              volume=150.0,
                              location=nunc_target_plate[Target_position[g]].bottom(1),
                              rate=10.0)
            right_pipette.blow_out(location=nunc_target_plate[Target_position[g]].bottom(1))
            if water_run:
                right_pipette.return_tip(home_after=False)
            else:
                right_pipette.drop_tip(home_after=False)
            g = g + 8

    def mixing_master_mix_and_sample():
        k = 0
        for j in range(int(len(Source_position) / 8)):
            right_pipette.pick_up_tip()

            right_pipette.mix(repetitions=5,
                              volume=120.0,
                              location=nunc_target_plate[Target_position[k]].bottom(),
                              rate=10.0)

            right_pipette.aspirate(10, nunc_target_plate[Target_position[k]].top(), rate=10.0)

            if water_run:
                right_pipette.return_tip(home_after=False)
            else:
                right_pipette.drop_tip(home_after=False)
            k = k + 8

    def water_run_prep():
        ### FOR PREPARATION ONLY NOT TO BE USED ON REAL RUN
        ## PREPARE FOR WATER RUN (ASPIRATE FROM RESERVOIR AND DISPENSE TO DW WITH MAGRACK)
        right_pipette.distribute(
            400.0,
            mm_source['A1'],
            [dna_source_plate.wells_by_name()[well_name] for well_name in Target_position],
            blow_out=True,
            blowout_location='source well'
        )

        # # #PREPARE FOR COLORING
        # right_pipette.distribute(
        #     50.0,
        #     mm_source['A1'],
        #     [dna_source_plate.wells_by_name()[well_name] for well_name in Target_position],
        #     blow_out=True,
        #     blowout_location='source well'
        # )
        # right_pipette.pick_up_tip()
        # right_pipette.mix(repetitions=20,
        #                   volume=200.0,
        #                   location=mm_source['A1'],
        #                   rate=10.0)
        #
        # if water_run:
        #     right_pipette.return_tip(home_after=False)
        # else:
        #     right_pipette.drop_tip(home_after=False)

    def clear_dna_plate():
        i = 0
        right_pipette.pick_up_tip()
        for j in range(int(len(Source_position) / 8)):
            right_pipette.aspirate(200, dna_source_plate[Source_position[i]].bottom(1))
            right_pipette.dispense(200, mm_source['A1'])
            i = i + 8

        if water_run:
            right_pipette.return_tip(home_after=False)
        else:
            right_pipette.drop_tip(home_after=False)

    #### COMMANDS ####
    if water_run:
        protocol.set_rail_lights(True)
    else:
        protocol.set_rail_lights(False)

    # IF YOU WANT TO CANCEL A STEP BELOW JUST ADD '#'
    only_sample_mixing()
    dna_aliquot()
    protocol.pause('Add Mastermix to resvoir')
    master_mix_aliquot()
