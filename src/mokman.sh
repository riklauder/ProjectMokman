#!/bin/bash

@echo off
python3 maptpy.py > layouts/randomMap0.lay
python3 maptpy.py > layouts/randomMap1.lay
python3 maptpy.py > layouts/randomMap2.lay
python3 maptpy.py > layouts/randomMap3.lay
python3 maptpy.py > layouts/randomMap4.lay
python3 maptpy.py > layouts/randomMap5.lay
python3 maptpy.py > layouts/randomMap6.lay
python3 maptpy.py > layouts/randomMap7.lay
python3 maptpy.py > layouts/randomMap8.lay
python3 maptpy.py > layouts/randomMap9.lay

./mapt > layouts/randomfMap.lay
python mokman.py