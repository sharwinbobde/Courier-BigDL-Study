from dataclasses import dataclass
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor


@dataclass
class Job:
    cpu: int
    njobs: int
    network: int


class Courier:
    """ Courier has 3 parameters to account for utilization, accuracy and response time,
    based on which, and their weights, it chooses the optimal batch size for the task

    labels are in format dict
    accuracy -> labels
    time -> labels
    utilization -> labels
    """

    def __init__(self, models: dict, scaler, alpha: float = 0.5, beta: float = 0.5, batches=[64, 128, 256, 512]):

        self.batches = np.array(batches).reshape(len(batches), 1)

        if alpha + beta != 1:
            raise ValueError('The hyperparameters need to add up to 1')

        # Configure the hyperparams and the training data
        self.alpha = alpha
        self.beta = beta

        self.scaler = scaler

        # Compute the predictors
        self.acc_model = models['accuracy']
        self.time_model = models['time']

    def optimize(self, job: Job, latency=None, test=False):
        """Find the best batch given the job and the latency
        If test is true, the features are just cpu, batch and network"""
        acc, t = self._predict(job, test)

        b = self.batches

        if latency:
            # Just take the options that satisfy the requirements
            fit = t[t < latency]
            if len(fit) == 0:
                print('Not a single value fulfills the '
                      'time requirements, selecting minimum time')
                # Return the minimum time
                min_t_idx = np.where(t == t.min())[0][0]
                return self.batches[min_t_idx], (acc[min_t_idx],
                                                 t[min_t_idx])

            else:
                acc = acc[t < latency]
                b = self.batches[t < latency]
                t = t[t < latency]

                # Return the best accuracy under that latency
                idx = np.where(acc == acc.max())[0][0]
                return b[idx], (acc[idx], t[idx])

        # Return the batch that better fulfills the requirements and
        # also return a tuple with the predictions
        sc_a = acc / np.max(acc)
        sc_t = 1 - (t / np.max(t))

        sc = self.alpha * sc_a + self.beta * sc_t

        # Get the index of the max score
        max_sc_idx = np.where(sc == sc.max())[0][0]
        return b[max_sc_idx], (acc[max_sc_idx],
                               t[max_sc_idx])

    def _fit_model(self, labels):
        """Fit the model to particular labels"""
        reg = self.model
        reg.fit(self.X, labels)
        return reg

    def _preprocess_data(self, X):
        """Standardizes the data"""
        scaler = StandardScaler()
        return scaler.fit_transform(X)

    def _predict(self, job: Job, test):
        """Predicts the time, accuracy and util with different batches
        and returns the best one given the optims"""

        acc = []
        t = []

        # predict the performance of the job with different batches
        for b in self.batches:
            if test:
                data_point = self.scaler.transform([[job.cpu, b, job.network]])
            else:
                data_point = self.scaler.transform([[job.cpu * job.njobs, job.cpu, job.njobs, b, job.network]])
            _acc = self.acc_model.predict(data_point)
            _t = self.time_model.predict(data_point)
            # print(f'Batch {b}, acc = {_acc} and t = {_t}')

            acc.append(_acc)
            t.append(_t)

        return np.array(acc), np.array(t)
