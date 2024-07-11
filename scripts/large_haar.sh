#!/bin/bash

# Loop 100 times
for i in {1..100}; do
	# Execute the commando
	build/ARM/gem5.opt emb/st_sim.py -c emb_exemplo/haar/large_haar  --cpu ARM_A72

	# Move and rename stats.txt
	mv m5out/stats.txt ~/results/
	cp ~/results/stats.txt ~/results/large_haar_$i.txt # Add counter to filename
	rm ~/results/stats.txt
done

echo "Done executing benchmark."
