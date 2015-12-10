# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 17:17:02 2015

@author: Navdeep Sharma
"""

"""
List of libraries imported for program
"""
import math
import numpy as np
import csv
from collections import defaultdict
import operator
from collections import Counter
import random

"""
global variables to be used in the program
"""
header = []
trainingData = []
testData = []

"""
buildData function takes file name as a input,
shuffle the data, divide data into traning and test samples.
"""
def buildData(filename):
    global header
    global trainingData
    global testData
    
    rows = csv.reader(open(filename))
    header = next(rows)
    data = []
    for row in rows:
        data.append(row)
    """
    Randomising data every time, for every model.
    """
    random.shuffle(data)
    data = np.array(data)
    cutOff = round(len(data) * 2 / 3)
    trainingData = data[:cutOff]
    testData = data[cutOff:]
    

"""
function to calculate the entropy and calculations for information gain
"""
def entropy(data, attributeIndex):
    classIndex = len(header) - 1
    entropyClass = {}
    entropy = 0
    
    """
    Entropy calculation of dataset
    """
    if classIndex == attributeIndex:
        for row in data:
            if row[classIndex] in entropyClass:
                entropyClass[row[classIndex]] += 1
            else:
                entropyClass[row[classIndex]] = 1
        for eachKey in entropyClass:
            entropy -= (entropyClass[eachKey] / len(data)) * math.log(entropyClass[eachKey] / len(data), 2)
        return entropy
        
    else:
        """
        Entropy calculation & part of information gain calculation,
        for attributes of the dataset.
        """
        for row in data:
            if row[attributeIndex] in entropyClass:
                if row[classIndex] in entropyClass[row[attributeIndex]]:
                    entropyClass[row[attributeIndex]][row[classIndex]] += 1
                else:
                    entropyClass[row[attributeIndex]][row[classIndex]] = 1
            else:
                entropyClass[row[attributeIndex]] = {}
                entropyClass[row[attributeIndex]][row[classIndex]] = 1
            #print (entropyClass)
        entropies = {}
        entropiesTotal = {}
        for eachKey in entropyClass:
            keytotal = 0
            entropies[eachKey] = 0
            for value in entropyClass[eachKey]:
                keytotal += entropyClass[eachKey][value]
            for value in entropyClass[eachKey]:
                entropies[eachKey] -= (entropyClass[eachKey][value] / keytotal) * math.log(entropyClass[eachKey][value] / keytotal, 2)
            entropiesTotal[eachKey] = keytotal
        for eachEntropy in entropies:
            entropy += ((entropiesTotal[eachEntropy] / len(data)) * entropies[eachEntropy])
        return entropy
    
"""
calculating information gain with the help of entropy function
"""    
def informationGain(attributeIndex):
    return entropy(trainingData, len(header) - 1) - entropy(trainingData, attributeIndex)
   
"""
dividing training dataset into instances to be passed to recursive
build_decision_tree function, based on attributes
"""
def getValuesForAttribute(data, attributeIndex):
    partitions = defaultdict(list)
    for instance in data:
        partitions[instance[attributeIndex]].append(instance)
    return partitions
   
"""
getting the attribute index, whose information gain is highest
among the attributes index range passed
"""   
def getHighestInfoGainAttribute(attributesIndexRange):
    allAttributesInfoGain = {}
    for i in attributesIndexRange:
        allAttributesInfoGain[i] = informationGain(i)
    allAttributesInfoGain = sorted(allAttributesInfoGain.items(), key=operator.itemgetter(1))
    return (allAttributesInfoGain[len(allAttributesInfoGain)-1][0])

"""
finding out the majority class based on the data passed
"""    
def majorityValueOfClassIndex(data, attributeIndex):
    majorityValuesCount = {}
    for instance in data:
        if instance[attributeIndex] in majorityValuesCount:
            majorityValuesCount[instance[attributeIndex]] += 1
        else:
            majorityValuesCount[instance[attributeIndex]] = 1
    majorityValuesCount = sorted(majorityValuesCount.items(), key=operator.itemgetter(1))
    return (majorityValuesCount[len(majorityValuesCount)-1][0])
        

"""
function to create decision tree or train the model
class_index - specify the class index in dataset
"""
def build_decision_tree(instances, 
                         candidate_attribute_indexes=None, 
                         class_index=0, 
                         default_class=None, 
                         trace=0):
   
                             
    '''Returns a new decision tree trained on a list of instances.
    
    '''
    if candidate_attribute_indexes is None:
        candidate_attribute_indexes = [i 
                                       for i in range(0, len(instances[0])) 
                                       if i != class_index]
 
    """
    finding class label count for construction of root node of tree
    """    
    class_labels_and_counts = Counter([instance[class_index] for instance in instances])
  
        
    if not candidate_attribute_indexes:
        if trace:
            print('{}Using default class {}'.format('< ' * trace, default_class))
        return default_class
    """
    If all the instances have the same class label, return that class label
    """
    if len(class_labels_and_counts) == 1:
        class_label = class_labels_and_counts.most_common(1)[0][0]
        #print ("class label:: ", class_label)
        if trace:
            print('{}All {} instances have label {}'.format(
                '< ' * trace, len(instances), class_label))
        return class_label
    else:
        default_class = majorityValueOfClassIndex(instances, class_index)
     
        """
        Choose the next best attribute index to best classify the instances
        """
        best_index = getHighestInfoGainAttribute(candidate_attribute_indexes)
        #print ("best index:: ", best_index)
        if trace:
            print('{}Creating tree node for attribute index {}'.format(
                    '> ' * trace, best_index))

        """
        Create a new decision tree node with the best attribute index 
        and an empty dictionary object (for now)
        """
        tree = {best_index:{}}
        #print ("tree:: ", tree)
        """
        Create a new decision tree sub-node (branch) for each of the values 
        in the best attribute field
        """
        partitions = getValuesForAttribute(instances, best_index)
  
        """
        Remove that attribute from the set of candidates for further splits
        """
        remaining_candidate_attribute_indexes = [i 
                                                 for i in candidate_attribute_indexes 
                                                 if i != best_index]
        #print ("remaining_candidate_attribute_indexes:: ", remaining_candidate_attribute_indexes)
        for attribute_value in partitions:
            if trace:
                print('{}Creating subtree for value {} ({}, {}, {}, {})'.format(
                    '> ' * trace,
                    attribute_value, 
                    len(partitions[attribute_value]), 
                    len(remaining_candidate_attribute_indexes), 
                    class_index, 
                    default_class))
                
            """
            Create a subtree for each value of the the best attribute
            """
            subtree = build_decision_tree(
                partitions[attribute_value],
                remaining_candidate_attribute_indexes,
                class_index,
                default_class,
                trace + 1 if trace else 0)
                
                tree[best_index][attribute_value] = subtree

    return tree

"""
function to classify the target class of the instance based on the model provided
"""
def classify(tree, instance, default_class=None):
    '''Returns a classification label for instance, given a decision tree'''
    if not tree:  # if the node is empty, return the default class
        return default_class
    if not isinstance(tree, dict):  # if the node is a leaf, return its class label
        return tree
    attribute_index = list(tree.keys())[0]  # using list(dict.keys()) for Python 3 compatibility
    attribute_values = list(tree.values())[0]
    instance_attribute_value = instance[attribute_index]
    if instance_attribute_value not in attribute_values:  # this value was not in training data
        return default_class
    # recursively traverse the subtree (branch) associated with instance_attribute_value
    return classify(attribute_values[instance_attribute_value], instance, default_class)

"""
Running the test 10 times, finding accuracy at each run
and the average accuracy
"""
averageAccuracy = 0
runs = 0
for i in range(1, 11):
    buildData("D:\DA\SEM1\ML\Assignment3\owls15.csv")
    tree = build_decision_tree(trainingData, class_index=len(header)-1)  # remove trace=1 to turn off tracing
    total = 0
    correct = 0
    runs += 1
    default_value = majorityValueOfClassIndex(testData, len(header)-1)
    confusionMatrix = {}
    for instance in testData:
        if instance[len(header)-1] not in confusionMatrix:
            confusionMatrix[instance[len(header)-1]] = {}
            
    for instance in testData:
        total += 1
        predicted_label = classify(tree, instance, default_value)
        actual_label = instance[len(header)-1]
        if predicted_label not in confusionMatrix[actual_label]:
            confusionMatrix[actual_label][predicted_label] = 1
        else:
            confusionMatrix[actual_label][predicted_label] += 1
        #print('predicted: {}; actual: {}'.format(predicted_label, actual_label))
        if(predicted_label == actual_label):
            correct +=1
    print ("\n\n")
    print ("Accuracy for Run-",i, "is:: ", round(((correct * 100) / total),2), "%" )
    
    averageAccuracy += ((correct * 100) / total)
    confusionHeader = "\t\t"
    for key in confusionMatrix:
        confusionHeader = confusionHeader + key + "\t"
    confusionHeader = confusionHeader + "<-- Predicted as"
    print (confusionHeader)
    for key1 in confusionMatrix:
        if key1 == "BarnOwl":
            confustionLine = key1 + "\t\t"
        else:
            confustionLine = key1 + "\t"
        
        for key2 in confusionMatrix:
            if key2 in confusionMatrix[key1]:
                if key2 == "SnowyOwl":
                    confustionLine = confustionLine + "\t" + str(confusionMatrix[key1][key2]) + "\t"
                else:
                    confustionLine = confustionLine + str(confusionMatrix[key1][key2]) + "\t"                    
            else:
                if key2 == "SnowyOwl":
                    confustionLine = confustionLine + "\t0\t"
                else:
                    confustionLine = confustionLine + "0\t"
        print (confustionLine)
print ("\n\n")
print ("Average accuracy for Classifier is:: ", round((averageAccuracy / runs),2), "%")