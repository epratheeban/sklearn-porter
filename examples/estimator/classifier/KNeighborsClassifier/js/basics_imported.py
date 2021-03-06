# -*- coding: utf-8 -*-

from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn_porter import Porter


iris_data = load_iris()
X = iris_data.data
y = iris_data.target

clf = KNeighborsClassifier(algorithm='brute',
                           n_neighbors=3,
                           weights='uniform')
clf.fit(X, y)

porter = Porter(clf, language='js')
output = porter.export(export_data=True)
print(output)

"""
if (typeof XMLHttpRequest === 'undefined') {
    var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
}

var KNeighborsClassifier = function(jsonFile) {
    this.data = undefined;

    var Neighbor = function(y, dist) {
        this.y = y;
        this.dist = dist;
    };

    var promise = new Promise(function(resolve, reject) {
        var httpRequest = new XMLHttpRequest();
        httpRequest.onreadystatechange = function() {
            if (httpRequest.readyState === 4) {
                if (httpRequest.status === 200) {
                    resolve(JSON.parse(httpRequest.responseText));
                } else {
                    reject(new Error(httpRequest.statusText));
                }
            }
        };
        httpRequest.open('GET', jsonFile, true);
        httpRequest.send();
    });

    var compute = function(temp, cand, q) {
        var dist = 0.,
            diff;
        for (var i = 0, l = temp.length; i < l; i++) {
    	    diff = Math.abs(temp[i] - cand[i]);
    	    if (q==1) {
    	        dist += diff;
    	    } else if (q==2) {
    	        dist += diff*diff;
    	    } else if (q==Number.POSITIVE_INFINITY) {
    	        if (diff > dist) {
    	            dist = diff;
    	        }
    	    } else {
    	        dist += Math.pow(diff, q);
            }
        }
        if (q==1 || q==Number.POSITIVE_INFINITY) {
            return dist;
        } else if (q==2) {
            return Math.sqrt(dist);
        } else {
            return Math.pow(dist, 1. / q);
        }
    };

    this.predict = function(features) {
        return new Promise(function(resolve, reject) {
            promise.then(function(data) {
                if (typeof this.data === 'undefined') {
                    this.data = data;
                    this.nTemplates = this.data.X.length;
                }
                var classIdx = 0, i, dist;
                if (this.data.nNeighbors == 1) {
                    var minDist = Number.POSITIVE_INFINITY;
                    for (i = 0; i < this.data.nTemplates; i++) {
                        dist = compute(this.data.X[i], features, this.data.power);
                        if (dist <= minDist) {
                            minDist = dist;
                            classIdx = this.data.y[i];
                        }
                    }
                } else {
                    var classes = new Array(this.data.nClasses).fill(0);
                    var dists = [];
                    for (i = 0; i < this.nTemplates; i++) {
                        dist = compute(this.data.X[i], features, this.data.power);
                        dists.push(new Neighbor(this.data.y[i], dist));
                    }
                    dists.sort(function compare(n1, n2) {
                        return (n1.dist < n2.dist) ? -1 : 1;
                    });
                    for (i = 0; i < this.data.kNeighbors; i++) {
                        classes[dists[i].y]++;
                    }
                    for (i = 0; i < this.data.nClasses; i++) {
                        classIdx = classes[i] > classes[classIdx] ? i : classIdx;
                    }
                }
                resolve(classIdx);
            }, function(error) {
                reject(error);
            });
        });
    };

};

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv[2].trim().endsWith('.json')) {

        // Features:
        var features = process.argv.slice(3);

        // Parameters:
        var json = process.argv[2];

        // Estimator:
        var clf = new KNeighborsClassifier(json);

        // Prediction:
        clf.predict(features).then(function(prediction) {
            console.log(prediction);
        });

    }
}
"""
