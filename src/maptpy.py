import Naked
from Naked.toolshed.shell import execute_js, muterun_js

result = execute_js('mapgen.js')

if result:
    # JavaScript is successfully executed
else:
    # JavaScript is failed
