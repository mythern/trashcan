# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

import random
import settings


class GeneticOperator(object):

    @staticmethod
    def mutate(genotype):
        """
        This genetic operator performs mutations on a genotype
        :param genotype: A bit vector
        """

        pos = random.randint(0, settings.GENOME_LENGTH - 1)
        genotype[pos] = int(not genotype[pos])

    @staticmethod
    def component_mutate(genotype):
        """
        This genetic operator performs a component mutation on a genotype
        :param genotype: A bit vector
        """

        from_point = random.randint(0, settings.GENOME_LENGTH - 1)
        to_point = random.randint(1, settings.GENOME_LENGTH)

        for i in range(min(from_point, to_point), max(from_point, to_point)):
            genotype[i] = int(not genotype[i])

    @staticmethod
    def int_mutate(genotype, m=1):
        for i in range(random.randint(1, settings.GENOME_MUTATION_INTENSITY)):
            pos = random.randint(0, settings.GENOME_LENGTH - 1)
            genotype[pos] = random.randint(0, m - 1)

    @staticmethod
    def int_component_mutate(genotype, m=1):
        from_point = random.randint(0, settings.GENOME_LENGTH - 1)
        to_point = random.randint(1, settings.GENOME_LENGTH)

        for i in range(min(from_point, to_point), max(from_point, to_point)):
            genotype[i] = random.randint(0, m - 1)

    @staticmethod
    def simple_int_crossover(genotype_one, genotype_two):
        s = random.randint(0, len(genotype_one))
        return genotype_one[:s] + genotype_two[s:], genotype_two[:s], genotype_one[s:]

    @staticmethod
    def crossover(genotype_one, genotype_two):
        """
        This genetic operator performs crossover on a pair of genotypes
        """

        slicepoints = set()
        while len(slicepoints) < settings.GENOME_CROSSOVER_POINTS:
            slicepoints.add(random.randint(0, len(genotype_one)))
        slicepoints = sorted(list(slicepoints))
        slicepoints.append(len(genotype_one))

        new_genotype_one = []
        new_genotype_two = []

        maintain = True
        old = 0
        while slicepoints:
            s = slicepoints.pop()
            if maintain:
                new_genotype_one.extend(genotype_one[old:s])
                new_genotype_two.extend(genotype_two[old:s])
            else:
                new_genotype_one.extend(genotype_two[old:s])
                new_genotype_two.extend(genotype_one[old:s])
            old = s

        return new_genotype_one, new_genotype_two


# Phenotype representation functions

class Phenotype(object):

    @staticmethod
    def translate_genotype_to_phenotype(genotype):
        """
        Translates a genotype representation into a phenotype representation
        :param genotype: A numpy bit array
        :return: A Phenotype representation of the genotype
        """

        return settings.PHENOTYPE_FUNCTION(genotype)

    @staticmethod
    def bitstring_phenotype(genotype):
        """
        Translates a genotype into a bitstring phenotype
        :param genotype: A list of 0's and 1's
        :return: A phenotype represented as a string of bit values (0 or 1)
        """

        return ''.join(map(str, map(int, genotype)))

    @staticmethod
    def integer_bitstring_phenotype(genotype):
        """
        Translates a genotype into a list of integers
        :param genotype: A list of 0's and 1's
        :return: A phenotype represented as a list of integer values
        """

        bitstring_ptype = Phenotype.bitstring_phenotype(genotype)
        phenotype = []
        for i in range(0, settings.GENOME_LENGTH, 6):
            phenotype.append(int(bitstring_ptype[i:i+6], 2) % settings.SURPRISING_SEQUENCE_S)

        return phenotype

    @staticmethod
    def integer_sequence_phenotype(genotype):
        return genotype[:]
