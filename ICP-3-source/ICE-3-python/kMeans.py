from pyspark import SparkContext
from pyspark import SparkConf
from numpy import array
from math import sqrt
from pyspark.mllib.clustering import KMeans

if __name__ == "__main__":

    # init spark program
    conf = SparkConf().setMaster("local")
    sc = SparkContext(conf=conf)

    # Load and parse data
    spatial_data = sc.textFile("3D_spatial_network.txt")
    parsed_data = spatial_data.map(lambda x: array([float(y) for y in x.split(',')]))

    print(parsed_data.collect())

    # Make data into 3 and 4 clusters
    clusters = KMeans.train(parsed_data, 3, maxIterations=10, initializationMode="random")
    clusters1 = KMeans.train(parsed_data, 4, maxIterations=10, initializationMode="random")

    # function for error
    def error(point):
        center = clusters.centers[clusters.predict(point)]
        return sqrt(sum([x ** 2 for x in (point - center)]))

    def error1(point):
        center = clusters1.centers[clusters1.predict(point)]
        return sqrt(sum([x ** 2 for x in (point - center)]))

    # Formula to get Within Set Sum of Squared Error
    wssse = parsed_data.map(lambda p: error(p)).reduce(lambda x, y: x+y)
    print("WSSSE = " + str(wssse))
    wssse1 = parsed_data.map(lambda p: error1(p)).reduce(lambda x, y: x+y)
    print("WSSSE1 = " + str(wssse1))

    # save to file
    clusters.save(sc, "3cluster")

    sc.stop()
