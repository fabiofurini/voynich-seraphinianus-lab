from pathlib import Path
import argparse,subprocess,sys
R=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--suite',choices=['matched','affixes','hierarchy','calibration','multiscale','boundary','substitution'],required=True);a=p.parse_args()
cmds={'matched':[['matched_backoff.py']],'affixes':[['affix_prediction.py'],['long_affix_prediction.py','3'],['long_affix_prediction.py','4']],'hierarchy':[['hierarchy_stronger.py']],'calibration':[['hierarchy_control.py'],['hierarchy_calibration.py']],'multiscale':[['multiscale.py']],'boundary':[['robust_boundary.py']]}
if a.suite=='substitution':subprocess.run([sys.executable,str(R/'research/Voynich_test_sostituzione/voynich_attack.py')],check=True)
else:
 for cmd in cmds[a.suite]:subprocess.run([sys.executable,str(R/'research/grammar_comparison'/cmd[0]),*cmd[1:]],check=True)
