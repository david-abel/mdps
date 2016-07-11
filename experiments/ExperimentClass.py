# Python libs.
import os
import sys
sys.path.append(os.getcwd() + "/..")
from collections import defaultdict

# Local libs.
from ExperimentParametersClass import ExperimentParameters
import chartUtils

class Experiment(object):
    ''' Experiment Class for Discrete MDP Experiments '''

    resultsDir = "../results/"

    def __init__(self, agents, mdp, params=None):
        self.agents = agents
        self.parameters = ExperimentParameters(params)
        self.mdp = mdp
        self.rewards = defaultdict(list)
        self.name = Experiment.resultsDir + str(self.mdp)
        self._setupFiles()

    def _setupFiles(self):
        if not os.path.exists(self.name + "/"):
            os.makedirs(self.name + "/")
        else:
            for agent in self.agents:
                if os.path.exists(self.name + "/" + str(agent) + ".csv"):
                    os.remove(self.name + "/" + str(agent) + ".csv")

    def makePlots(self):
        chartUtils.makePlots(self.name, self.agents)

    def addExperience(self, agent, s, a, r, sprime):
        self.rewards[agent] += [r]

    def endOfEpisode(self, agent):
        self.writeEpisodeRewardToFile(agent, sum(self.rewards[agent]))

    def endOfInstance(self, agent):
        '''
        Summary:
            Adds a new line to indicate we're onto a new instance.
        '''
        out_file = open(self.name + "/" + str(agent) + ".csv", "a+")
        out_file.write("\n")
        out_file.close()

    def writeEpisodeRewardToFile(self, agent, r):
        # Write reward.
        out_file = open(self.name + "/" + str(agent) + ".csv", "a+")
        out_file.write(str(r) + ",")
        out_file.close()

    def writeToFile(self):
        '''
        Summary:
            Writes relevant experiment information to a file for reproducibility.
        '''
        # Make the subdirectory if it doesn't yet exist.
        new_dir = self.name
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        
        # Write.
        out_file = open(new_dir + "/parameters.txt", "w+")
        toFile = self._getExpFileString()
        out_file.write(toFile)
        out_file.close()

    def _getExpFileString(self):
        '''
        Returns:
            (str): contains the AGENT-names, the MDP-names, and PARAMETER-information.
        '''
        agentString = "AGENTS: "
        for agent in self.agents:
            agentString += str(agent)

        agentString += "\n\n"
        mdpString = "MDP: " + str(self.mdp) + "\n\n"
        paramString = "PARAMS: " + str(self.parameters) + "\n\n"

        return agentString + mdpString + paramString
