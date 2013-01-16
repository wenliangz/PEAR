#! /usr/bin/env python
import os 
import glob
import copy
import math
import random 
from subprocess import call

def find_accuracy(fn_truth, fn_assemby, name, method = "panda", printnice = True):
	numseqs = 0
	numassebled = 0
	numcorrect = 0
	ftruth = open(fn_truth)
	seq_len_map = {}
	line = ftruth.readline()
	while line!="":
		ss = line.strip().split()
		seq_len_map[ss[0]] = int(ss[1])
		numseqs = numseqs + 1
		line = ftruth.readline()
	ftruth.close()
	
	fin = open(fn_assemby)
	line = fin.readline()
	while line!="":
		seqname = line.strip()
		if method == "shera":
			seqname = seqname[1:].split("_")[0]
			seq = fin.readline().strip()
			as_seq_len = len(seq)
			true_seq_len = int(seq_len_map[seqname])
			numassebled = numassebled + 1
			if true_seq_len == as_seq_len:
				numcorrect = numcorrect + 1
		else:
			if method == "panda":
				seqname = seqname[1:].split(":")[0]
				print(seqname)
			elif method == "flash":
				seqname = seqname[1:]
			else:
				seqname = seqname[1:].split("/")[0]
			seq = fin.readline().strip()
			fin.readline()
			qual = fin.readline().strip()
			as_seq_len = len(seq)
			true_seq_len = int(seq_len_map[seqname])
			numassebled = numassebled + 1
			if true_seq_len == as_seq_len:
				numcorrect = numcorrect + 1
		line = fin.readline()
	fin.close()
	
	if numseqs == 0:
		numseqs = 1
	if numassebled == 0:
		numassebled = 1
	
	if printnice:
		print("Assebly method:" + method)
		print("Total seqs:" + repr(numseqs))
		print("Assembled seqs:" + repr(numassebled))
		print("Corrected seqs:" + repr(numcorrect))
		print("Cor / Total:" + repr(float(numcorrect)/float(numseqs)))
		print("Cor / Assemled:" + repr(float(numcorrect)/float(numassebled)))
	else:
		if numcorrect == 0:
			numcorrect = numseqs - numassebled
			print(name + "	" +repr(numseqs)+"	"+repr(numassebled)+"		"+repr(numcorrect)+"	"+repr(float(numcorrect)/float(numseqs))+"	" + repr(float(numcorrect)/float(numseqs)) + "	" +  repr(1- float(numcorrect)/float(numseqs)))
		else:
			print(name + "	" +repr(numseqs)+"	"+repr(numassebled)+"		"+repr(numcorrect)+"	"+repr(float(numcorrect)/float(numseqs))+"	" + repr(float(numcorrect)/float(numassebled)) + "	" +  repr(1- float(numcorrect)/float(numassebled)))
	
	return numcorrect

def test_pear(forward, reverse, output, pvalue, minoverlap, maxlen, minlen, mintrimlen, minquality, maxuncalled, scoremethod, empirical_freqs, truelenfile, testname, testw):
	if empirical_freqs == "yes":
		call(["../src/pear","-f",forward,"-r",reverse,"-o", output,"-p", pvalue, "-v", minoverlap, "-m", maxlen, "-n", minlen, "-t", mintrimlen, "-q", minquality, "-u", maxuncalled, "-s", scoremethod, "-e", "-g", testw])
	else:
		call(["../src/pear","-f",forward,"-r",reverse,"-o", output,"-p", pvalue, "-v", minoverlap, "-m", maxlen, "-n", minlen, "-t", mintrimlen, "-q", minquality, "-u", maxuncalled, "-s", scoremethod, "-g", testw])
	return find_accuracy(fn_truth = truelenfile, fn_assemby = output+".assembled.fastq", name = testname, method = "pear", printnice = False)

def publication_data():
	print("Testname" + "	" +"Reads"+"	"+"Assembled"+"	"+"Correct"+"	"+"Correct/Reads"+"		" + "Correct/Assembled" + "	fp_rate")
	num101bpt_nt = test_pear(forward = "16S_101bp1.fq.through.fastq", 
						  reverse = "16S_101bp2.fq.through.fastq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_101bp_len.txt", 
						  testname = "101bpt_nt",
						  testw = "1")
	num101bpt_t01 = test_pear(forward = "16S_101bp1.fq.through.fastq", 
						  reverse = "16S_101bp2.fq.through.fastq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_101bp_len.txt", 
						  testname = "101bpt_t01",
						  testw = "1")
	num101bp_nt = test_pear(forward = "16S_101bp1.fq", 
						  reverse = "16S_101bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_101bp_len.txt", 
						  testname = "101bp_nt",
						  testw = "1")
	num101bp_t01 = test_pear(forward = "16S_101bp1.fq", 
						  reverse = "16S_101bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_101bp_len.txt", 
						  testname = "101bp_t01",
						  testw = "1")
	num101bp_nt = test_pear(forward = "16S_150bp1.fq", 
						  reverse = "16S_150bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_150bp_len.txt", 
						  testname = "150bp_nt",
						  testw = "1")
	num101bp_t01 = test_pear(forward = "16S_150bp1.fq", 
						  reverse = "16S_150bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_150bp_len.txt", 
						  testname = "150bp_t01",
						  testw = "1")
	num101bp_nt = test_pear(forward = "16S_165bp1.fq", 
						  reverse = "16S_165bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_165bp_len.txt", 
						  testname = "165bp_nt",
						  testw = "1")
	num101bp_t01 = test_pear(forward = "16S_165bp1.fq", 
						  reverse = "16S_165bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_165bp_len.txt", 
						  testname = "165bp_t01",
						  testw = "1")
	num101bp_nt = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_nt",
						  testw = "1")
	num101bp_t01 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t01",
						  testw = "1")
	num101bp_nt = test_pear(forward = "16S_190bp1.fq", 
						  reverse = "16S_190bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_190bp_len.txt", 
						  testname = "190bp_nt",
						  testw = "1")
	num101bp_t01 = test_pear(forward = "16S_190bp1.fq", 
						  reverse = "16S_190bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_190bp_len.txt", 
						  testname = "190bp_t01",
						  testw = "1")
	num101bp_nt = test_pear(forward = "16S_250bp1.fq", 
						  reverse = "16S_250bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_250bp_len.txt", 
						  testname = "250bp_nt",
						  testw = "1")
	num101bp_t01 = test_pear(forward = "16S_250bp1.fq", 
						  reverse = "16S_250bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_250bp_len.txt", 
						  testname = "250bp_t01",
						  testw = "1")
						  
	num101bp_nt = test_pear(forward = "16S_165bp1.fq", 
						  reverse = "16S_165bp2.fq", 
						  output = "165bpplot", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "0", 
						  maxuncalled = "1", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_165bp_len.txt", 
						  testname = "165bp_nt",
						  testw = "1")



def main():
	#101bp through, should have corrected assembled sequences = 
	print("Testname" + "	" +"Reads"+"	"+"Assembled"+"	"+"Correct"+"	"+"Correct/Reads"+"		" + "Correct/Assembled" + "	fp_rate")
	num101bpt_nt = test_pear(forward = "16S_101bp1.fq.through.fastq", 
						  reverse = "16S_101bp2.fq.through.fastq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_101bp_len.txt", 
						  testname = "101bpt_nt",
						  testw = "1")
	num101bpt_t1 = test_pear(forward = "16S_101bp1.fq.through.fastq", 
						  reverse = "16S_101bp2.fq.through.fastq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_101bp_len.txt", 
						  testname = "101bpt_t1",
						  testw = "1")
	num101bpt_t2 = test_pear(forward = "16S_101bp1.fq.through.fastq", 
						  reverse = "16S_101bp2.fq.through.fastq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_101bp_len.txt", 
						  testname = "101bpt_t2",
						  testw = "2")
	num101bpt_t1_ne = test_pear(forward = "16S_101bp1.fq.through.fastq", 
						  reverse = "16S_101bp2.fq.through.fastq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "no", 
						  truelenfile = "16S_101bp_len.txt", 
						  testname = "101bpt_t1_ne",
						  testw = "1")
	num101bp = test_pear(forward = "16S_101bp1.fq", 
						  reverse = "16S_101bp2.fq", 
						  output = "to1", 
						  pvalue = "0.001", 
						  minoverlap = "10", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_101bp_len.txt", 
						  testname = "101bp_t2_001",
						  testw = "2")
	num150bp_nt = test_pear(forward = "16S_150bp1.fq", 
						  reverse = "16S_150bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_150bp_len.txt", 
						  testname = "150bp_nt",
						  testw = "1")
	num150bp_t1 = test_pear(forward = "16S_150bp1.fq", 
						  reverse = "16S_150bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_150bp_len.txt", 
						  testname = "150bp_t1",
						  testw = "1")	
	num150bp_t2 = test_pear(forward = "16S_150bp1.fq", 
						  reverse = "16S_150bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_150bp_len.txt", 
						  testname = "150bp_t2",
						  testw = "2")	
	num165bp_nt = test_pear(forward = "16S_165bp1.fq", 
						  reverse = "16S_165bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_165bp_len.txt", 
						  testname = "165bp_nt",
						  testw = "1")
	num165bp_t1 = test_pear(forward = "16S_165bp1.fq", 
						  reverse = "16S_165bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_165bp_len.txt", 
						  testname = "165bp_t1",
						  testw = "1")	
	num165bp_t2 = test_pear(forward = "16S_165bp1.fq", 
						  reverse = "16S_165bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_165bp_len.txt", 
						  testname = "165bp_t2",
						  testw = "2")
	num165bp_t1_o10 = test_pear(forward = "16S_165bp1.fq", 
						  reverse = "16S_165bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "10", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_165bp_len.txt", 
						  testname = "165bp_t1_o10",
						  testw = "1")	
	num180bp_nt = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_nt",
						  testw = "1")	
	num180bp_nt_m2 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "2", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_nt_m2",
						  testw = "1")
	num180bp_nt = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "3", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_nt_m3",
						  testw = "1")
	num180bp_t1 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t1",
						  testw = "1")	
	num180bp_t2 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t2",
						  testw = "2")	
	num180bp_t1_o10 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "10", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t1_o10",
						  testw = "1")
	num180bp_t1_05 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.05", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t1_05",
						  testw = "1")
	num180bp_t1_001 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.001", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t1_001",
						  testw = "1")
	num180bp_t1_05 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.05", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t2_05",
						  testw = "2")
	num180bp_t2_001 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.001", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t2_001",
						  testw = "2")
	num180bp_t1_m2 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "2", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t1_m2",
						  testw = "1")
	
	num180bp_t1_m3 = test_pear(forward = "16S_180bp1.fq", 
						  reverse = "16S_180bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "3", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_180bp_len.txt", 
						  testname = "180bp_t1_m3",
						  testw = "1")
						  
	num190bp_t2 = test_pear(forward = "16S_190bp1.fq", 
						  reverse = "16S_190bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_190bp_len.txt", 
						  testname = "190bp_t1",
						  testw = "1")	
	num190bp_t2 = test_pear(forward = "16S_190bp1.fq", 
						  reverse = "16S_190bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_190bp_len.txt", 
						  testname = "190bp_t2",
						  testw = "2")	
	num190bp_nt = test_pear(forward = "16S_190bp1.fq", 
						  reverse = "16S_190bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_190bp_len.txt", 
						  testname = "190bp_nt",
						  testw = "2")	
	num250bp_t1 = test_pear(forward = "16S_250bp1.fq", 
						  reverse = "16S_250bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_250bp_len.txt", 
						  testname = "250bp_t1",
						  testw = "1")	
	num250bp_t2 = test_pear(forward = "16S_250bp1.fq", 
						  reverse = "16S_250bp2.fq", 
						  output = "to1", 
						  pvalue = "0.01", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_250bp_len.txt", 
						  testname = "250bp_t2",
						  testw = "2")	
	num250bp_nt = test_pear(forward = "16S_250bp1.fq", 
						  reverse = "16S_250bp2.fq", 
						  output = "to1", 
						  pvalue = "1.0", 
						  minoverlap = "1", 
						  maxlen = "500", 
						  minlen = "50", 
						  mintrimlen = "50", 
						  minquality = "10", 
						  maxuncalled = "0.05", 
						  scoremethod = "1", 
						  empirical_freqs = "yes", 
						  truelenfile = "16S_250bp_len.txt", 
						  testname = "250bp_nt",
						  testw = "2")
		 
	os.remove("to1.assembled.fastq")
	os.remove("to1.discarded.fastq")
	os.remove("to1.unassembled.forward.fastq")
	os.remove("to1.unassembled.reverse.fastq")
	
	
	if 	(num101bpt_t1 == 33068 and 
		num150bp_t2 == 28228 and 
		num165bp_t1_o10 == 26413 and 
		num180bp_t1 == 20483 and 
		num180bp_t1_001 == 17341 and
		num180bp_t2_001 == 15532 and 
		num180bp_t1_m2 == 20459 and 
		num180bp_t1_m3 == 20242 and 
		num190bp_nt == 17075 and 
		num250bp_t2 == 23060):
			print("Tests passed!")
	else:
		print("Warnning: tests failed!")				  
	

#main()
publication_data()
