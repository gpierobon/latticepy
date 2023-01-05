
switch = False

# This allows to run the simulation like this
# python3 main.py $NDIMS $N $DEV ...
if switch == True:
    '''
    NDIMS     = int(sys.argv[1]) 
    N         = int(sys.argv[2])
    DEV       = sys.argv[3]
    PREC      = sys.argv[4]
    VERB      = sys.argv[5]
    ICTYPE    = sys.argv[]
    ICFILE    = sys.argv[]
    L         = float(sys.argv[])
    dt        = float(sys.argv[])
    t         = float(sys.argv[])
    tf        = float(sys.argv[])
    G         = float(sys.argv[])
    '''
else:
    NDIMS     = 3
    N         = 256
    DEV       = 'gpu'
    PREC      = 'single'
    VERB      = 'normal'
    ICTYPE    = 'solitons'
    ICFILE    = 'solitons.txt'
    L         = 1                           
    dt        = L/N/4.                     # Timestep
    t         = 0                          # Initial time 
    tf        = 0.5                        # Final time
    G         = 4000                       # Newton's constant   
