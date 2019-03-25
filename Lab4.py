#Gilbert Velasquez
# CS2302 MW 1:30-2:50
# lab 4
# Instructor Olac Fuentes
# TA Anindita Nath and Maliheh Zargaran
# Date of Last Modification 3/24/2019
#The purpose of this lab was to get used to B-Trees. We learned about the 3 types of routes to tackle problems using B-Trees. And given an outline for each type it 
#was easy to convert them to do the desired task once I figured out which type I need to use. In this code there is a method for: Computing the height of a B-Tree, Turning a B-Tree into a sorted list,
# Getting the smallest element at a given depth, getting the largest element at a given depth, getting the number of nodes at a given depth, printing all the items at a given depth, getting the number of full nodes,
# getting the number of full leaves, And finding the depth of a given element. This Lab taught me that sometimes the answers arent as complicated as they seem. It also showed me the importance of knowing how to traverse 
# a B_tree. Knowing how to traverse a B_Tree was essential for all of these methods. Using the logic gained from BST find smallest and largest is also made simple.




class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)

def Height(T):
    if T.isLeaf:
        return 0
    return 1 + Height(T.child[0])

def ExtractTree(T,L):
    if T.isLeaf: #appends every element to list once we reach the leaf
        for t in T.item:
            L.append(t)
    else:
        for i in range(len(T.item)): # Traverses the List in order to get the sorted list
            ExtractTree(T.child[i],L)
            L.append(T.item[i])
        ExtractTree(T.child[len(T.item)],L)    

def SmallestAtDepth(T,d): #Returns the smallest item at a given depth 
    if d==0:
        return T.item[0] #will return the item in index 0 since that is the smallest 
    if T.isLeaf:
        return math.inf # returns infinity if we go out of bounds 
    return SmallestAtDepth(T.child[0],d-1) # recur until we are at the desired depth 

def LargestAtDepth(T,d): # returns the largest item at a given depth
    if d ==0:
        return T.item[len(T.item)-1] # will return the item in the last index since that is the biggest 
    if T.isLeaf:
        return math.inf # returns infinty if we go out of bounds 
    return LargestAtDepth(T.child[len(T.item)],d-1) # recur until we are at the desired depth 

def NumNodesAtDepth(T,d): # counts number of nnodes at a given depth 
    if d == 0: # if our orignal d is 0
        return 1
    if d-1 == 0: # number of nodes at a depth is equal to the number of children from the level above. So we get to that level and return the number of children 
        return len(T.child)*2
    else:
        for i in range(len(T.child)):
            return NumNodesAtDepth(T.child[i],d-1) 
    
    
def PrintAtDepth(T,d): #prints items at a depth 
    if d==0: # once we are desired depth print only those nodes 
        for i in range(len(T.item)):
            print(T.item[i], end = " ")
    else:
        if not T.isLeaf: #recur with each child and the next depth 
            for i in range(len(T.child)):
                PrintAtDepth(T.child[i],d-1)


def FullNodes(T): # returns number full nodes in a B-Tree
    if len(T.item) == T.max_items: #if the node is full 
        return 1
    if T.isLeaf:
        return 0
    else:
        count = 0 # keep track of full nodes 
        for i in range(len(T.item)):
            count = count + FullNodes(T.child[i]) #traverse the B-Tree
    return count
        

def FullLeaves(T): # returns number of full leaves in a B-Tree
    if len(T.item) == T.max_items: #check if it's full 
        if T.isLeaf:
            return 1 # if it's a leaf then we keep track
        else:
            return 0 # if not we return 0 since it's not full 
    else:
        count = 0
        for i in range(len(T.item)):
            count = count + FullNodes(T.child[i]) #Traverse the B-Tree
    return count
    
    
def FindDepth(T,k): #Returns the Depth of a given key
    if k in T.item: 
        return 0
    if T.isLeaf: # Key wasnt in B-Tree
        return -1
    if k > T.item[-1]:
        d = FindDepth(T.child[-1],k) #if k is greater than the biggest element in the list go only to the right side 
    else:
        for i in range(len(T.item)):
            if k < T.item[i]:
                d = FindDepth(T.child[i],k)
    if d == -1:
        return -1
    return d + 1



L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,200,2,4,5,1,1,2]
T = BTree()    
for i in L:
    print('Inserting',i)
    Insert(T,i)
    PrintD(T,'') 
    #Print(T)
    print('\n####################################')

print(Height(T))
print(SmallestAtDepth(T,1))
print(LargestAtDepth(T,2))
print(PrintAtDepth(T,2))
print(FullNodes(T))
print(FullLeaves(T))
print(FindDepth(T,200))
print(NumNodesAtDepth(T,2))
L= []
ExtractTree(T,L)
print(L)