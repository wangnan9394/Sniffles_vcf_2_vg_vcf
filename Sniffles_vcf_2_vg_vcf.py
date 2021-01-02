import os
import argparse

parser = argparse.ArgumentParser(description = 'input ngmlr_vcf, output vg validation vcf', add_help = False, \
    usage = ' -i [input.vcf] -n [genome name] ')
required = parser.add_argument_group()
optional = parser.add_argument_group()
required.add_argument('-i', '--input', metavar = '[input.vcf]', help = 'vcf file', required = True)
required.add_argument('-g', '--genome', metavar = '[genome name]', help = 'genome name', required = True)

args = parser.parse_args()

genome=args.genome
input=args.input

cmd_mkdir='mkdir {}'.format(input[:-4])
cmd_cp1='cp {} {}'.format(genome,input[:-4])
cmd_cp2='cp {} {}'.format(input,input[:-4])
cmd_cd='cd {}'.format(input[:-4])
os.system(cmd_mkdir)
os.system(cmd_cp1)
os.system(cmd_cp2)
os.system(cmd_cd)
os.chdir(input[:-4])
os.getcwd()
def ngmlr_vcf_2_normal_vcf(originalfile):
    #cmd_pre1 = 'rm DB02_ngmlr.new.vcf'
    #cmd_pre2 = 'rm tmp1.txt'
    #cmd_pre3 = 'rm tmp2.txt'
    #os.system(cmd_pre1)
    #os.system(cmd_pre2)
    #os.system(cmd_pre3)
    outfilename=originalfile[:-4]+'.normal.vcf'
    outfile=open(outfilename,'a')
    with open(originalfile,'r') as f:
        ID=0
        for line in f:
            if line.startswith('##'):
                line3=line.split()
                line2=str(line3[0])+'\n'
                outfile.write(line2)
            if line.startswith('#CHROM'):
                outfile.write(line)
            if not line.startswith('#'):
                line=line.split()
                line7=(line[7].split(';'))[0]
                if  len(line[4]) >20 or len(line[3])>20:             
                    if line7 == "PRECISE" and line[6]=="PASS":
                        cmd_1 = 'samtools faidx {} {}:{}-{} > tmp1.txt'.format(genome,line[0],line[1],line[1])
                        os.system(cmd_1)
                        var1=os.popen('tail -n 1 tmp1.txt').read()
                        var=var1.replace("\n",'').replace('\t','')
                        cmd_2 = 'samtools faidx {} {}:{}-{} > tmp2.txt'.format(genome,line[0],line[1],str(int(line[1])+9))
                        os.system(cmd_2)
                        var2=os.popen('tail -n 1 tmp2.txt').read()
                        var3=var2.replace("\n",'').replace('\t','')
                        if not var==[]:
                            #print(len(line[3]),len(line[4]))
                            if len(line[3]) ==1:
                                #print(var1)
                                pos=line[1]
                                seq=var+line[4]
                                if seq[0]==var:
                                    ID+=1
                                    new_ll=[]
                                    new_ll.append(line[0])
                                    new_ll.append(pos)
                                    new_ll.append(str(ID))
                                    new_ll.append(var)                   
                                    new_ll.append(seq)
                                    new_ll.append(line[5])
                                    new_ll.append(line[6])
                                    new_ll.append('.')
                                    new_ll.append(line[8])
                                    new_ll.append(line[9])
                                    ll=''
                                    for i in new_ll:
                                        ll+=str(i)+'\t'
                                    ll1=ll+'\n'
                                    outfile.write(ll1)
                            if len(line[4])==1:
                                pos=line[1]
                                seq=line[3]
                                if seq[:10]==var3:
                                    ID+=1
                                    new_ll=[]
                                    new_ll.append(line[0])
                                    new_ll.append(pos)
                                    new_ll.append(str(ID))
                                    new_ll.append(seq)
                                    new_ll.append(var)
                                    new_ll.append(line[5])
                                    new_ll.append(line[6])
                                    new_ll.append('.')
                                    new_ll.append(line[8])
                                    new_ll.append(line[9])
                                    ll=''
                                    for i in new_ll:
                                        ll+=str(i)+'\t'
                                    ll1=ll+'\n'
                                    outfile.write(ll1)
##run step1
ngmlr_vcf_2_normal_vcf(input)
print("normal done!!")

def clear_vcf(filename):
    for i in range(100):
        print("round",str(i+1))
        cmd_0 = 'vg construct -r sjg_v2.fa -v {} 1>test.vg 2>error'.format(filename)
        os.system(cmd_0)
        cmd_alt='cat error'
        os.system(cmd_alt)
        with open('error','r') as f:
            lines = f.readlines()
            last_line=lines[-1]
            #print(last_line)
            error_position=last_line.replace(' ','').split('indexed:')
            error_position=error_position[-1].replace('\n','')
            #print(error_position)
            number='\''+'/'+error_position+'/'+'d'+'\''
            #print(number)
        cmd_1='sed -i {} {}'.format(number,filename)
        os.system(cmd_1)
        if error_position.isnumeric()==False:
            break
##run step2
clear_vcf(input[:-4]+'.normal.vcf')
print("clear done!!")

def sort_vcf(filename):
    new_filename = filename[:-4]+'.sort.vcf'
    cmd_s1='chr_order="chrMnchr1nchr2nchr3nchr4nchr5nchr6nchr7nchr8nchr9nchrUn"'
    os.system(cmd_s1)
    cmd_s2='cat {} | grep "^#" > header.vcf'.format(filename)
    os.system(cmd_s2)
    cmd_s3='cat {} | grep -v "^#" | sort -k1,1 -k2,2n > pre.sorted.vcf'.format(filename)
    os.system(cmd_s3)
    cmd_s4='cat header.vcf pre.sorted.vcf >{}'.format(new_filename)
    os.system(cmd_s4)
##run step3
sort_vcf(input[:-4]+'.normal.vcf')
print("sort done!!")

def reduce_vcf(filename):
    readDir = filename
    writeDir = filename[:-4]+'.reduce.vcf'
    outfile=open(writeDir,"w")
    f = open(readDir,"r")
    pos_seen = set()  # Build an unordered collection of unique elements.
    for line in f:
        line = line.strip('\n')
        line2=line.split('\t')
        if len(line2)==1:
            outfile.write(line +'\n')
        if len(line2)>1:
            pos = line2[1]
            if pos not in pos_seen:
                outfile.write(line+ '\n')
                pos_seen.add(pos)               
##run step4
reduce_vcf(input[:-4]+'.normal.sort.vcf')
print("reduce done!!")

##run step5 check
clear_vcf(input[:-4]+'.normal.sort.reduce.vcf')
size = os.path.getsize('error')
if size == 0:
    print('Susceed!')
else:
    print('Faild')