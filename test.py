import subprocess

CAThetaCutBarrel = 0.003
CAThetaCutForward = 0.004
dcaCutInnerTriplet = 0.16
dcaCutOuterTriplet = 0.26

#process

output = subprocess.run(['cmsRun','step3_RAW2DIGI_RECO_VALIDATION_DQM.py', 
                f'CAThetaCutBarrel={CAThetaCutBarrel}',
                f'CAThetaCutForward={CAThetaCutForward}',
                f'dcaCutInnerTriplet={dcaCutInnerTriplet}',
                f'dcaCutOuterTriplet={dcaCutOuterTriplet}'],
                capture_output=True)

print(output.stdout)
