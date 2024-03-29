import math
import random
    
def generator(distr_map):
    """ Returns a function that can be called to return a random value
        from the given distribution. 
        
        The map must have the form:
            { value: probability of being selected,
              next_value: probability of being selected,
              ... }

        Usage example:
            f = generator({3: 0.40,
                           4: 0.20,
                           5: 0.40})
            rand_val = f()
            next_rand_val = f()
    """
    def generate():
        rand = random.random()
        lower_bound = 0
        for value, probability in distr_map.iteritems():
            if lower_bound == 0:
                # this is the first iteration, and it's possible
                # rand could be 0 so we do a special if statement
                if rand <= probability:
                    return value
            else:
                if lower_bound < rand <= (lower_bound + probability):
                    return value
            lower_bound += probability
    return generate
    
def uniform(a, b):
    """ Returns a random number from the uniform distribution [a, b]
    """
    # python's random() returns a number from [0, 1)
    return int(random.random() * (b - a + 1)) + a
    
def bernoulli(p):
    """ Returns either 0 (fail) or 1 (success) given probability of success p
    """
    rand = random.random()
    if rand > p:
        return 0
    else:
        return 1
        
def exponential(lambda_):
    """ Returns duration of time between events given rate of arrival lambda_
    """
    if lambda_ == 0:
    	return 0
    rand = random.random()
    return -1 / lambda_ * math.log(1-rand)

def poisson(t, lambda_):
    """ Returns number of events in time t given rate lambda_
    """
    if lambda_ == 0:
    	return 0
    time = 0
    num_events = 0
    while time < t:
        time += exponential(lambda_)
        if time < t:        
            num_events += 1
    return num_events

def erlang(k, lambda_):
    """ Returns a duration of time for k events to happen given rate of
        arrival lambda_
    """
    time = 0
    num_events = 0
    while num_events < k:
        time += exponential(lambda_)
        num_events += 1
    return time
    
def coin_toss():
    """ Returns True or False with a 50/50 chance of either occurring """
    if bernoulli(0.5):
        return True
    return False
    
def normal(u, sigma):
    """ Returns a value from the specified normal distribution N(mu, sigma)
    """
    r1 = random.random()
    r2 = random.random()
    z = math.sqrt((-2.0 * math.log(r1))) * math.cos(2 * math.pi * r2)
    x = u + sigma * z 
    return x
