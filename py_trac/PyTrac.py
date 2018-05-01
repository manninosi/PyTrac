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

  out_index += 1;
  sstring =  '|' + str(out_index) + '\t\t\t|' + str(NPS) + '\t\t\t|' + str(cell_number) + '\t\t\t|' + str(energy) + '\n';

  return sstring;


# def process_expriment(NPS, reaction_types, cell_numbers, event_infos, event_count, outFile):
#   global acceptable_cell_number

#   is_accepted = 1;

#   ''' start of filtering '''

#   if not (checkNumber(reaction_types[event_count-1], acceptable_end_reaction_types)):
#     is_accepted = 0;

#   if is_accepted == 1:
#     for i in range(0, event_count):
#       if not (checkNumber(cell_numbers[i], acceptable_cell_number)):
#         is_accepted = 0;
#         break;

#   ''' end of filtering '''

#   if is_accepted == 1:
#     outFile.write(getPrintString(NPS, reaction_types, cell_numbers, event_infos, event_count));

# def check_validity(sample):
#
#   global acceptable_cell_number;
#
#   cell_numbers = sample['cell_numbers'];
#   event_count = sample['event_count'];
#   event_infos = sample['event_infos'];
#
#
#   if checkExistance(cell_numbers, acceptable_cell_number):
#     energy = 0;
#     indecies = getExistanceIndecies(cell_numbers, acceptable_cell_number);
#     indecies_len = len(indecies);
#     NPS = sample['NPS'];
#     if indecies_len == event_count:
#       ''' all cell_numbers is acceptable '''
#       info = event_infos[0];
#       energy = float(info[6]);
#     elif indecies_len > 0:
#       for i in range(0,indecies_len):
#         info = event_infos[indecies[i]];
#         energy = energy + float(info[6]);
#         if indecies[i]+1 < event_count:
#           info = event_infos[indecies[i]+1];
#           energy = energy - float(info[6]);
#
#     return (NPS, energy, 1 if energy > 0 else 0);
#
#   return (0, 0, 0);


# def process_experiments(collection, outFile):
#
#   print ('start processing ............');
#
#   collection_len = len(collection);
#
#   print ('len of collection:' + str(collection_len))
#
#   for i in range(0,collection_len):
#     (NPS, energy, validity) = check_validity(collection[i]);
#     if validity == 1:
#       ''' write into file: '''
#       outFile.write(getPrintString(NPS, energy));



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
    for line in open(adr):
        size_counter += 1

        ###SECTION OF CODE TO CLEAR OUT COLLECTION VARIABLE TO PREVENT MEMORY OVERFLOW ERROR
        if size_counter > 10**6: #Increase this value to make individual file writes larger
            print "Clearing variable cache and writing data file..."
            counter_outFile.write('total sample count: ' + str(sample_counter) + ' / abnormal sample count: ' + str(abnormality_counter)+'\n');
            outAdr = os.getcwd() + '/' + args[2] + "file_"+str(file_count);
            outFile = open(outAdr, 'w');
            writeHead(outFile);
            process_experiments(collection, outFile);
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
            if Flag_Term == 1:
                Flag_Term = 0


                if Line_Number <= 1: #Only surface crossing

                    continue
                else:
                    Line_Number = 0
                    count += 1
                    collection.append([count, NPS, Energy,Cell] )
                    Energy = 0
                    NPS = 0
                    #Append ID, NPS, Energy, Cell
                continue


            if particle[1] == '3000':#Check for 3000 to indicate a new particle being run
                Interaction = 'None'
                Line_Number = 0 #Keep track of interactions

                NPS = int(particle[0])
                continue
            #Check for different intereactions
            if particle[3] == '-3': #Photoelectric
                Interaction = "Photoelectric"
                Cell = int(particle[5])
                Line_Number +=1
                continue

            elif particle[3] == '-1': #Compton
                Interaction = "Compton"
                Cell = particle[5]
                Line_Number +=1
                continue
            else:

                if particle[0] in ['9000', '5000']:
                    Flag_Term = 1 #Particle has ended
                    Line_Number += 1
                    continue
                elif particle[0] in ['3000', '4000']:
                    Line_Number += 1
                    continue
                else: #Go to lines that contain energy values
                    if Interaction == "None":
                        Intial_Energy = float(particle[6])
                        Energy = float(particle[6]) #Should capture initial energy

                    elif Interaction == "Compton":
                        Energy -= float(particle[6])
                    elif Interaction == "Photoelectric" and float(particle[6]) < Intial_Energy: #Compton scatter occurred before Photoelectric
                        Energy += float(particle[6])
                    else:
                        Energy = float(particle[6])



    #         if  particle_len > 1:
    #             if particle_len <= newDataLen:
    #                 sample_counter = sample_counter + 1
    #                 if event_count > 0 and encounter_error == 0:
    #
    #                     sample = {};
    #
    #                     sample.setdefault('NPS', 0);
    #                     sample['NPS'] = NPS;
    #
    #                     sample.setdefault('reaction_types', 0);
    #                     sample['reaction_types'] = reaction_types;
    #                     sample.setdefault('cell_numbers', 0);
    #                     sample['cell_numbers'] = cell_numbers;
    #
    #                     sample.setdefault('event_infos', 0);
    #                     sample['event_infos'] = event_infos;
    #
    #                     sample.setdefault('event_count', 0);
    #                     sample['event_count'] = event_count;
    #                     # print "sample"
    #                     # print "\n"
    #                     # print sample
    #                     # print "particle\n"
    #                     # print particle
    #                     # sys.exit()
    #                     collection.append(sample);
    #
    #
    #
    #                 ''' reset variables '''
    #                 encounter_error = 0;
    #                 counter = 0;
    #                 event_count = 0;
    #                 reaction_types = [];
    #                 cell_numbers = [];
    #                 event_infos = [];
    #                 event_count = 0;
    #
    #                 # try:
    #                 NPS = int(particle[0]);
    #                 # except:
    #                 #   print line;
    #                 #   sys.exit();
    #
    #             else:
    #                 if counter % 2 == 1:
    #                     # try:
    #                     print "Paritlc\n"
    #                     print particle
    #                     reaction_types.append(int(particle[0]));
    #                     cell_numbers.append(int(particle[5]));
    #                     # except:
    #                     #   print line;
    #                     #   sys.exit();
    #                 else:
    #                     event_count = event_count + 1;
    #                     event_infos.append(particle);
    #
    #                     # except:
    #                     #   abnormality_counter = abnormality_counter + 1;
    #                     #   encounter_error = 1;
    #         counter += 1
    #
    #
    #
    # print 'end of collecting data ... total sample count: ' + str(sample_counter) + ' / abnormal sample count: ' + str(abnormality_counter);
    #
    # counter_outFile.write('total sample count: ' + str(sample_counter) + ' / abnormal sample count: ' + str(abnormality_counter)+'\n');
    #
    # print ('start processing collection ...')
    #
    # outAdr = os.getcwd() + '/' + args[2] + "file_"+str(file_count);
    # outFile = open(outAdr, 'w');
    # writeHead(outFile);
    # process_experiments(collection, outFile);

    print collection[0:10]
if __name__ == "__main__":
    main(sys.argv)
