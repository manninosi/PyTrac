import sys
import os
import re

acceptable_cell_number = [600];
acceptable_end_reaction_types = [9000, 4000, 5000];
"""
##Need to look for 4th column values
-1: Compton Scattering
-3: Photoelectric
-2: Rayleight (DONT CARE)

The energy on the line is the energy of the particle leaving the cell. Thus if "-3"
Just take the initial value. If "-1" do Initial - Final energy. Only need to look
at the last line. Can ignore "9000".

How to output data:
Interaction #, NPS, Cell, Energy
"""
out_index = 0;
ignoreLine = 10;
abnormality_counter = 0;
sample_counter = 0;

# def checkNumber(number, acceptable_numbers):
#     length = len(acceptable_numbers);
#     for i in range(0, length):
#         if number == acceptable_numbers[i]:
#             return True;
#
#     return False;
#
# def checkExistance(given_list, acceptable_numbers):
#   length = len(acceptable_numbers);
#   for i in range(0, length):
#     if acceptable_numbers[i] in given_list:
#       return True;
#
#   return False;
#
# def getExistanceIndecies(given_list, acceptable_numbers):
#
#   indecies = [];
#   length = len(given_list);
#   for i in range(0, length):
#     if checkNumber(given_list[i], acceptable_numbers):
#       indecies.append(i);
#
#   return indecies;
#
def writeHead(outFile):

  outFile.write('|ID\t\t\t|NPS\t\t\t|Cell_Number\t\t\t|Energy(MeV)\n');
#
def getPrintString(NPS, energy, out_index, cell_number):


  sstring =  '|' + str(out_index) + '\t\t\t|' + str(NPS) + '\t\t\t|' + str(cell_number) + '\t\t\t|' + str(energy) + '\n';

  return sstring;


def main(args):


    ''' sample code for calling this program: python lily.py 31_Kev_X-ray_Test.txt out.txt '''
    file_count = 1
    adr = os.getcwd() + '/' + args[1];  ''' input file address'''
    outAdr = os.getcwd() + '/' + args[2] + "file_"+str(file_count);
    try:
        ignoreLine = int(args[3]);
    except:
        ignoreLine = 10;

    outFile = open(outAdr, 'w');
    counter_outFile = open(outAdr+'_counter.counter', 'w');

    writeHead(outFile);

    counter = 0;
    newDataLen = 3;

    NPS = [];
    Energy = []
    Cell = []

    reaction_types = [];
    cell_numbers = [];
    event_infos = [];
    event_count = 0;
    ignore_counter = 0;

    collection = [];

    encounter_error = 0;
    size_counter = 0
    count = 0
    Flag_Term = 0
    Compton_Flag = 0
    Particles = 0
    Interaction_3000 = 0

    NPS_Check = []
    for line in open(adr):
        size_counter += 1

        ###SECTION OF CODE TO CLEAR OUT COLLECTION VARIABLE TO PREVENT MEMORY OVERFLOW ERROR
        if size_counter > 10**6: #Increase this value to make individual file writes larger
            print "Clearing variable cache and writing data file..."
            counter_outFile.write('total sample count: ' + str(sample_counter) + ' / abnormal sample count: ' + str(abnormality_counter)+'\n');
            outAdr = os.getcwd() + '/' + args[2] + "file_"+str(file_count);
            outFile = open(outAdr, 'w');
            writeHead(outFile);
            #process_experiments(collection, outFile);
            for i in collection:
                 outFile.write(getPrintString(i[1], i[2], i[0], i[3]))

            collection = []
            size_counter = 0
            file_count += 1
            ####


        ignore_counter += 1
        if ignore_counter > ignoreLine:

            ''' processing the line '''
            line = line.strip(); ''' remove whitespace of the start of each line '''
            line = re.sub(" +", " ", line);  ''' remove whitespace among the line using regular expression (+ mean it should contain one for sure) '''

            ''' extracting information '''
            particle = line.rstrip().split(' '); ''' this line seprate data that exist in one line and represent them as an array (particle) '''
            #print "New Line \n"
            # print particle
            particle_len = len(particle);
            if particle[0] == '3000':
                Interaction_3000 += 1
            if Flag_Term == 1:
                Flag_Term = 0


                if Line_Number == 0: #Only surface crossing

                    continue

                elif Compton_Flag == 1:
                    Energy += float(particle[6])
                    Line_Number = 0
                    count += 1
                    Compton_Flag = 0

                    collection.append([count, NPS, Energy,Cell] )
                    Energy = 0
                    Initial_Energy = 0
                    NPS = 0
                else:
                    Line_Number = 0
                    count += 1

                    collection.append([count, NPS, Energy,Cell] )
                    Energy = 0
                    Initial_Energy = 0
                    NPS = 0
                    #Append ID, NPS, Energy, Cell
                continue


            if particle[1] == '3000':#Check for 3000 to indicate a new particle being run
                Interaction = 'None'
                Line_Number = 0 #Keep track of interactions
                Particles += 1
                NPS = int(particle[0])
                NPS_Check.append(NPS)

                continue
            #Check for different intereactions
            if particle[3] == '-3' and particle[0] != '9000': #Photoelectric
                Interaction = "Photoelectric"
                Cell = int(particle[5])
                Line_Number +=1
                continue

            elif particle[3] == '-1' and particle[0] != '9000': #Compton
                Interaction = "Compton"
                Cell = int(particle[5])
                Line_Number +=1
            elif particle[3] == '-2':
                Interaction = "Rayleigh"
                # if particle[0] == '9000':
                #     pass
                # else:
                #
                #     continue
            else:

                if particle[0] in ['9000', '5000']:
                    if Interaction == "Compton":
                        Compton_Flag = 1


                    Flag_Term = 1 #Particle has ended
                    Line_Number += 1

                    continue
                elif particle[0] in ['3000', '4000']:
                    Line_Number += 1
                    continue
                else: #Go to lines that contain energy values
                    if Interaction == "None":

                        Initial_Energy = float(particle[6])
                        Energy = float(particle[6]) #Should capture initial energy
                    elif Interaction == "Rayleigh":
                        Energy = Energy

                    elif Interaction == "Compton":

                        Energy -= float(particle[6])
                    elif Interaction == "Photoelectric": #Compton scatter occurred before Photoelectric
                        if Compton_Flag == 1:
                            Energy += float(particle[6])
                        else:
                            Energy = Initial_Energy

                    else:
                        Energy = float(particle[6])




    print ('start processing collection ...')
    #
    outAdr = os.getcwd() + '/' + args[2] + "file_"+str(file_count);
    outFile = open(outAdr, 'w');
    writeHead(outFile);
    #process_experiments(collection, outFile);
    for i in collection:
         outFile.write(getPrintString(i[1], i[2], i[0], i[3]))


    size_counter = 0
    file_count += 1


    """
    SECTION OF CODE BELOW WAS USED TO DEBUG PTRAC PARSING DATA
    """
    for i in range(len(collection)):

        if collection[i][2] < 0:
            print "NPS with negative Energy"
            print collection[i][1]
    collection = []
    # q = 0
    # for i in range(len(collection)):
    #     t = i + q
    #     if collection[i][1] != NPS_Check[t]:
    #         q += 1
    #         print "NPS not showing up\n"
    #         print "Collection values\n"
    #         print collection[i]
    #         print "NPS values"
    #         print NPS_Check[t]
    #
    # print "Total New Particles\n"
    # print Particles
    # print "Length of Collection\n"
    # print len(collection)
    # print collection[400:700]
    # #print collection[55200:55500]# Checking event 1116528; appears to be writing that particle
    # print "Last entry in collection\n"
    # print collection[-1]
    # print "Times 3000 shows up in first entry\n"
    # print Interaction_3000
if __name__ == "__main__":
    main(sys.argv)
