import sys; args = sys.argv[1:]
file = open(args[0])
import math

def transfer(t_funct, input):
   if t_funct == "T1":
      return input
   
   elif t_funct == "T2":
      return input if input > 0 else 0
      
   elif t_funct == "T3":
      return 1 / (1 + math.e**(-input))
   
   else:
      return -1 + 2 / (1 + math.e**(-input))

def dot_product(input, weights, stage):
   return sum([float(weights[i + stage * len(input)]) * input[i] for i in range(len(input))])

def evaluate(file, input_vals, t_funct):
   weight_list = []
   x_vals = [input_vals]
   
   for line in file.read().splitlines():
      weight_list.append(line.split(" "))
   
   for i in range(1, len(weight_list)):
      x_vals.append([0] * (len(weight_list[i - 1]) // len(x_vals[i - 1])))
   
   for layer in range(1, len(x_vals)):
      for stage in range(len(x_vals[layer])):
         x_vals[layer][stage] = transfer(t_funct, dot_product(x_vals[layer - 1], weight_list[layer - 1], stage))
   
   return [x_vals[-1][stg] * float(weight_list[-1][stg]) for stg in range(len(x_vals[-1]))]
     
def main():
   inputs, t_funct, transfer_found = [], 'T1', False
   
   for arg in args[1:]:
      if not transfer_found:
         t_funct, transfer_found = arg, True
      else:
         inputs.append(float(arg))
         
   li = (evaluate(file, inputs, t_funct)) #ff
   
   for x in li:
      print (x, end = " ") # final outputs
       
if __name__ == '__main__': main()

# Dennis Tislin, Period 5, 2026