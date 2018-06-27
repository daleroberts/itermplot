import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
iris = sns.load_dataset("iris")
species = iris.pop("species")
g = sns.clustermap(iris)
plt.show()
