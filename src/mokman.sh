#!/bin/sh

@echo off
node mapgen.js > layouts/randomMap0.lay
node mapgen.js > layouts/randomMap1.lay
node mapgen.js > layouts/randomMap2.lay
node mapgen.js > layouts/randomMap3.lay
node mapgen.js > layouts/randomMap4.lay
node mapgen.js > layouts/randomMap5.lay
node mapgen.js > layouts/randomMap6.lay
node mapgen.js > layouts/randomMap7.lay
node mapgen.js > layouts/randomMap8.lay
node mapgen.js > layouts/randomMap9.lay


./mapt > layouts/randomfMap.lay
python mokman.py