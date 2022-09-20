### 1 General Description
This assignment is one part of a multi-part project to build some simplified components of the Ethereum
blockchain. The first task is to build a data structure that can store addresses (accounts) and their balances
on the chain. Its most important property is that validation of information should be efficient and relatively
lightweight, such that determining this validity is easier than recomputing the full structure.
In Ethereum, this role is filled by the Merkle Patricia Tree (MPT). For this assignment, we will ignore
the Patricia portion of the structure, and ask you to build a Merkle tree that stores and hashes account
data in a way similar to the MPT. In future assignments, you will use this structure to create a block of
addresses, add it to a chain, and lookup and validate specific information as a light node would.
For this assignment, you will build a simple Merkle tree over a set of addresses and their corresponding
balances, provided by a sorted input file. Below, I describe the format of the Merkle tree, explain the use
of a Java implementation of SHA-256, and provide additional specifics on program function and output.
Although the SHA-256 discussion is in terms of Java, you are free to use other languages, but you will need
to provide me a simple “turnkey” way to run your code, collect source code for Moss, and comply with
specified input/output formats.
We shall be using the sunlab as our test environment so that we have a common, standard platform. You
may develop on your own machines, but in the end, you’ll need to test in the sunlab. Obviously, this means
that you are restricted to use programming languages supported in the default sunlab environment.
The project will be done in groups (see Section 5). The groups will persist for future assignments.
###### 2 Details

#### 2.1 Input
You shall prompt for a file name containing the input. The format of the input file is plain text (i.e., a
.txt format file). We plan to give all test files a .txt extension but your code should be robust to other file
names. The input file will represent a list of addresses, and their balance on the blockchain. Each line will
consist of a string (representing an address), a single space, and an integer. Lines will be null-terminated.
The input files will have their lines sorted alphabetically by address, with addresses only appearing once per
file. Each address will contain only characters from the hexadecimal alphabet (0..9, a..f) and are guaranteed
to have no special characters or white-space. Addresses are a fixed length of 40 characters, and balances
will be non-negative integers sufficiently small enough to fit within the limits of your chosen programming
language.
An example line appears as follows:
fc91428771e2b031cd46b0478ce20a7af0b110d4 1311994
There will be no test data provided since it is easy for you to generate your own test data.

### 2.2 Tree Structure
While we won’t need to navigate through the tree in the traditional sense, we still need to have some sort
of index from which we can calculate the Merkle root. You are free to accomplish however you like, but
generally you will need a data structure to hold the follow information for each account:
1. address: a string
2. balance: an integer
3. the SHA-256 hash of account and balance, concatenated
You will need to be able to traverse all the accounts, sorted by their addresses (again, use the structure
of your choice, an array would suffice, but may make your job more difficult).

### 2.3 SHA-256
You are free to use existing implementations of SHA-256. Credit your source in a comment (if it is not obvious
as it would be in Java). If you are using Java, you will find a SHA-256 implementation in the MessageDigest
class. Import “java.security.MessageDigest” and instantiate a MessageDIgest object as follows:
MessageDigest messd = MessageDigest.getInstance("SHA-256");
More details can be found online, for example https://www.geeksforgeeks.org/sha-256-hash-in-java/
For other languages, you will need to either write your own SHA-256 function or find one online. If you
use an online source, be sure to cite that source in a comment at the start of your code.

### 2.4 Calculating a Merkle root
In order to calculate a Merkle root, you must build a Merkle tree from the bottom up, with the accounts
serving as the leaves. This tree is guaranteed to be a complete and balanced binary tree, but it may not
necessarily be full.
Parent nodes will have their SHA-256 hash calculated by concatenating the hashes of their two children,
and hashing the resulting string. If the parent only has one child, then its hash is the hash of that child.
Your program should output a single line, which should be the hash at the “root” node of your tree (the
Merkle root). Remember, the input file is sorted alphabetically, so your program should produce the same
root each time.