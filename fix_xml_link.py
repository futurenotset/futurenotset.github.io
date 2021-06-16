import os
import sys
import re
from glob import glob


def main(src, debuf=False):
    
    files = glob(f'{src}/**/*.*ml', recursive=True)                               

    for file in files:                                                            
        #dst_file = re.sub(src, dst, file)                                        
        dst_file = file                                                           
        if debug:
            dst_file =  dst_file + ".tmp"                                                          
        if os.path.isfile(file):                                                  
            #print(file)                                                          
            if re.search('podlove/image', file):                                  
                continue                                                          

            if re.search('html', file) or re.search('xml', file):                 
                try:                                                              
                    f = open(file, 'r', encoding="utf-8")                         
                    lines = f.readlines()                                         
                    f.close()                                                     
                except:                                                           
                    print(file)                                                   
                    exit()                                                        
                                                                                  
                f = open(dst_file, 'w', encoding="utf-8")                     
                for line in lines:                                                
                    g = re.search('href="(http[\w\/\.:]+)"', line)                
                    if g and re.search("feed", line):                             
                        murl = g.group(1)                                         
                        nurl = f'{g.group(1)}index.xml'                           
                        if not re.search("xml$", murl):                           
                            line = re.sub(murl, nurl, line)                       
                                                                                  
                    g = re.search('(<span class="theme-credit">.+</span>)', line) 
                    if g:                                                         
                        print(g.group(1))                                        
                        line = re.sub(g.group(1), "", line)                       
                                                                                  
                    f.write(line)                                                 
                                                                                  

                f.close()                                                         

if __name__ == "__main__":
    if 0 == len(sys.argv):
        pass                                                                  
    elif 1 == len(sys.argv):
        src = os.getcwd()                                                              
    elif 2 == len(sys.argv):
        src = sys.argv[1]
    else:
        raise Exception()
    print(src)
    debug = False
    main(src, debug)
