def modifiedzeroin3033803361(f, int, params):
  #Inputs
  #  -a mathematical function
  #    -f
  #  -an interval object containing a left endpoint and right endpoint
  #    -int.a
  #    -int.b
  #  -a paramater object containing root and function tolerance and max iterations
  #    -params.root_tol
  #    -params.func_tol
  #    -params.maxit
  #Outputs
  #  -a root of f that is within root or function tolerance
  #    -root
  #  -an info object
  #    -info.flag
  def sign_of_product(left, right):
    #This function returns 1 if a*b > 1 and -1 if a*b < 1 and 0 otherwise
    if left > 0:
      a = 1
    if left < 0:
      a = -1
    if right > 0:
      b = 1
    if right < 0:
      b = -1
    return a * b

  def bisect_part2(a, b, fa, fb): 
    #update c
    c = (a+b)/2
    fc = f(c)
    #check if we are done.
    done = False
    if abs(fc) < params.func_tol or b - a < params.root_tol:
       done = True
    #update x's
    x0, x1, x2, f0, f1, f2 = a, b, c, fa, fb, fc
    return done, x0, x1, x2, c, f0, f1, f2, fc 
    
  def bisect(f, a, b, c, fa, fb, fc):
    #This function should perform a single bisection step
    #It will return what it thinks the new interval should be 
    if sign_of_product(fa, fc) == -1:
      new_a = a
      new_b = c
      new_fa = fa
      new_fb = fc
    else:
      new_a = c
      new_b = b
      new_fa = fc
      new_fb = fb
    return new_a, new_b, new_fa, new_fb

  def IQI(x0, x1, x2, f0, f1, f2):
    #This function should perform a single IQI step
    #It will return the new x value
    return (f1*f2*x0)/((f0-f1)*(f0-f2)) + (f0*f2*x1)/((f1-f0)*(f1-f2)) + (f0*f1*x2)/((f2-f0)*(f2-f1))

  class Info:
    def __init__(self):
      self.flag = 0
    def update(self):
      self.flag = 1

  #Lets initialize our base conditions:  
  a = int.a
  fa = f(a)
  b = int.b
  fb = f(b)
  c = (a+b)/2
  fc = f(c)
  x0, x1, x2, f0, f1, f2 = a, b, c, fa, fb, fc
  few = 3
  some = 3
  current_iteration = 1
  previous_fx3_values = []
  info = Info()
  #Lets check if we are already done:
  if abs(fa) < params.func_tol:
    return a, info
  if abs(fb) < params.func_tol:
    return b, info
  if abs(fc) < params.func_tol:
    return c, info
  #Alright now we can really get started:
  while(current_iteration < params.maxit):
    x3 = IQI(x0, x1, x2, f0, f1, f2)
    #if x3 is out of the interval we perform some bisection steps
    if x3 < a or x3 > b:
      previous_fx3_values = []
      for i in range(some):
        a, b, fa, fb = bisect(f, a, b, c, fa, fb, fc)
        done, x0, x1, x2, c, f0, f1, f2, fc =  bisect_part2(a, b, fa, fb)
        if done: return x2, info
    #otherwise, x3 was in the interval, so lets call f
    else:
      f3 = f(x3)
      previous_fx3_values.append(f3) 
      #check if we are done
      if abs(f3) < params.func_tol: return x3, info
      #update x's
      x0, x1, x2, f0, f1, f2 = x1, x2, x3, f1, f2, f3
      #now lets update our bounds
      three = [(x0,f0), (x1,f1), (x2,f2) ]
      three.sort()
      (left_x,f_left) = three[0]
      (right_x,f_right) = three[2]
      if sign_of_product(fa, f_right) == -1:
        b = right_x
        fb = f_right
      elif sign_of_product(f_left, fb) == -1:
        a = left_x
        fa = f_left
    #now lets check if we are getting closer
      length = len(previous_fx3_values)
    #do we even have enough previous consecutive IQI calls?
      if length > few:
        recent = previous_fx3_values[length-1]
        previous = previous_fx3_values[length-(few+1)]
        #did IQI decrease too slowly? if yes, switch to bisect
        if (abs(recent) / abs(previous)) > 0.5:
          #then we perform some bisect steps
          previous_fx3_values = []
          for i in range(some):
            a, b, fa, fb = bisect(f, a, b, c, fa, fb, fc)
            done, x0, x1, x2, c, f0, f1, f2, fc =  bisect_part2(a, b, fa, fb)
            if done: return x2, info
            
    #root_tol stoppin check
    if b - a < params.root_tol:
      return c, info
    #update iteration
    current_iteration += 1
  return False, info.update()