import os
import sys
import re
from glob import glob
from shutil import copytree, ignore_patterns

def main(src, debug=False):
    
    #domain = {'futurenotset.com': 'future.wp.podonaut.com'}
    domain = {'futurenotset.podonaut.com': 'futurenotset.com'}
    #domain = {'example.com': None}
    files = glob(f'{src}/**/*.*', recursive=True)                               


    for src_file in files:                                                            
        dst_file = src_file
        if os.path.isfile(src_file) and re.search("ml$", src_file):                                                  
            #print(file)                                                          
            if re.search('podlove/image', src_file):                                  
                continue                                                          

            if re.search('html', src_file) or re.search('xml', src_file):                 
                try:                                                              
                    f = open(src_file, 'r', encoding="utf-8")                         
                    lines = f.readlines()                                         
                    f.close()                                                     
                except:                                                           
                    print(src_file)                                                   
                    exit()                                                        
                                                                              
                f = open(dst_file, 'w', encoding="utf-8")                     
                for line in lines:                                                
                    g = re.search('"(http[\w\/\\\.:]+)"', line)                
                    if g and re.search("feed", line):                             
                        murl = g.group(1)                                         
                        murl = re.sub("\\\\", "\\\\\\\\", murl)                                            
                        
                        nurl = f'{g.group(1)}index.xml'                           
                        if not re.search("xml$", murl):                           
                            #print(g.span())
                            #print(murl)
                            #print(nurl)
                            line = re.sub(murl, nurl, line)                       
                                                                                  
                    g = re.search('(<span class="theme-credit">.+</span>)', line) 
                    if g:                                                         
                        #print(g.group(1))                                        
                        line = re.sub(g.group(1), "", line)                       
                    f.write(line)                                                 
                                                                                      

                f.close()                                                         
        
    for d in domain:
        print(d)
        if domain[d] is None:
            dst = src
        else:
            dst = f"{src}/../{domain[d]}"
            copytree(src, dst, ignore=ignore_patterns(".git"), dirs_exist_ok=True)
        
        print(src)
        print(dst)
        #continue
        for src_file in files:                                                            
            dst_file = re.sub(src, dst, src_file) 
            #print(src_file)
            #print(dst_file)
            
            if os.path.isfile(src_file) and re.search("ml$", src_file):                                                  
                #print(file)                                                          
                if re.search('podlove/image', src_file):                                  
                    continue                                                          

                f = open(src_file, 'r', encoding="utf-8")                         
                lines = f.readlines()                                         
                f.close()  
                                                                   
                if re.search('html', src_file) or re.search('xml', src_file):                 
                    print(src_file)
                    print(dst_file)
                    f = open(dst_file, 'w', encoding="utf-8")                     
                    for line in lines:                                                
                        g = re.search(f'http[s\/\\\.:{d}]', line)
                        if g:   
                            line = re.sub(d, domain[d], line)
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
    debug = True
    main(src, debug)
