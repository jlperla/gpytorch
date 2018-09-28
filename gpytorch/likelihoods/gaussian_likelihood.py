from __future__ import absolute_import, division, print_function, unicode_literals

import math
import torch
from ..distributions import MultivariateNormal
from ..functions import add_diag
from ..likelihoods import Likelihood


class GaussianLikelihood(Likelihood):
    r"""
    """
    def __init__(self, log_noise_prior=None):
        super(GaussianLikelihood, self).__init__()
        self.register_parameter(
            name="log_noise", parameter=torch.nn.Parameter(torch.tensor([0.])), prior=log_noise_prior
        )

    def forward(self, input):
        if not isinstance(input, MultivariateNormal):
            raise ValueError("GaussianLikelihood requires a MultivariateNormal input")
        mean, covar = input.mean, input.lazy_covariance_matrix
        noise = add_diag(covar, self.log_noise.exp())
        return input.__class__(mean, noise)

    def variational_log_probability(self, input, target):
        res = -0.5 * ((target - input.mean) ** 2 + input.variance) / self.log_noise.exp()
        res += -0.5 * self.log_noise - 0.5 * math.log(2 * math.pi)
        return res.sum(0)
