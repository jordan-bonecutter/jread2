import json
import os
import re
import fnmatch
import argparse


from drawtree import draw_tree

def main():
  project_dir = os.path.dirname(os.path.realpath(__file__))
  output_dir = os.path.join(project_dir, 'res/img')
  input_dir = os.path.join(project_dir, 'res/json_files')
  parser = argparse.ArgumentParser()
  parser.add_argument('--filename', help='file name or list of file names in directory set by --input-dir argument. Use * to include all file', nargs='+', type=str)
  parser.add_argument('--output-dir', '-d', help='Output directory for generated plots', type = str, default= output_dir)
  parser.add_argument('--input-dir','-p',  help='Path to the directory of json files.', type=str, default=input_dir)
  args = parser.parse_args()
  input_files = []
  if (args.filename != None):
    for item in args.filename:
      if item.find("*") >= 0:
         for f in os.listdir(args.input_dir):
           if fnmatch.fnmatch(f,item):
             try:
               input_files.append(open(os.path.join(args.input_dir, f)))
             except:
               print "cannot open file: " + os.path.join(args.input_dir , f) + " in wildcard. try --help for more information"
               return
             
      else:
        try:
          input_files.append(open(os.path.join(args.input_dir , item), "rU"))
        except:
          print "file: " + os.path.join(args.input_dir , item) + " is not exist. try --help for more information"
          return
  if (len(input_files) == 0):
    print "at least one file should be given"
    return
  
  for f in input_files:
    try:
      data = json.load(f)
      print os.path.join(f.name) 
      draw_tree(data['snapshots'][0]['tree_full'], os.path.join(args.output_dir, 'full_tree/', '.'.join(f.name.split("/")[-1].split(".")[:-1])))
      draw_tree(data['snapshots'][0]['tree_trim'], os.path.join(args.output_dir, 'combined_tree/', '.'.join(f.name.split("/")[-1].split(".")[:-1])))

    except(KeyboardInterrupt, SystemExit):
      raise
    except:
      print "Error dumping:", os.path.join(args.input_dir, f.name) 

if __name__ == "__main__" :
  main()


