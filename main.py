# Re is imported in order to split based on multiple parts simply
import re

# Not a valid IP error message definition
def dCallingNotAValidIP():
    # Here is what will be displayed if an incorrect thing, like a letter or a symbol, was put in by the user
    sRestartInput=input("{} was inputted, this is not a real IPv4 address, would you like to restart. Enter \"Yes\" or \"No\" ".format(sIPAddressInput))
    # The if block checks if the user would like to restart by saying yes or no
    # Checks if yes or y was put in by the user for them to restart and then if it is it will restart
    if sRestartInput.casefold()=="yes" or sRestartInput.casefold()=="y":
        print("Restarting")
        Input()
        CheckingInputLength()
        CheckingClassType()
        SpecificRanges()
        Binary()
    # If yes was not put in by the user it will check if no or n was put in and stop the script while displaying "Exiting script"
    elif sRestartInput.casefold()=="no" or sRestartInput.casefold()=="n":
        print("Exiting script")
        exit()
    # if neither of these cases was put in by the user it will tell them that it was not yes or no and ask them again
    else:
        print("Yes or No was not inputted")
        dCallingNotAValidIP()

# This section exists so that the scripts can exit with an ending message, this will be called when quit is put in by the user
def dEndScript():
    print("{} was inputted, the program will end.".format(sIPAddressInput))
    exit()

# This section will take in the input from the user, and then it will check if the person put in quit or if that did not happen it will
# Split (by periods commas and spaces) what the person put in, and then it will check if there are leading zeros in what the user put in
# and tell the person if there are any
def Input():
    global sIPAddressInput, lIPAddressSplit
    # The program will ask the user for an IP address, and strip the trailing white space
    sIPAddressInput=input("Please enter an IPv4 address in dotted decimal (it can be separated by periods spaces and commas). Or enter the word \"quit\" or \"q\" to quit: ").strip()
    # The program checks if the input was quit
    if sIPAddressInput.casefold()=="quit" or sIPAddressInput.casefold()=="q":
        # The script starts over
        dEndScript()
    # The program will split the IP address into different parts in order for it to interpret them
    # as well as converting the input into an int
    else:
        # Reference: https://stackoverflow.com/questions/21023901/how-to-split-at-all-special-characters-with-re-split
        lIPAddressSplit=re.split(r"[ ,.]", sIPAddressInput)
        # This section will check if there are leading zeros in front of a number
        iToCount = 0
        # This will loop through all the Octs
        for OctNumber in lIPAddressSplit:
            NumberOfLeadingZeros=len(OctNumber) - len(OctNumber.lstrip('0'))

            # This will be called if there are multiple or leading zeros and tell the person if that happens
            def dIN():
                try:
                    if lIPAddressSplit[iToCount][NumberOfLeadingZeros].isdigit:
                        print("There were leading zeros with a number after it, ", end="")
                        dCallingNotAValidIP()
                    else:
                        print("Unexpected Error, ", end="")
                        dCallingNotAValidIP()
                except Exception as e:
                    pass
                print("There were leading zeros, ", end="")
                dCallingNotAValidIP()

            # This will check if you can move on to the part that will "classify" the IP address
            def dEND():
                if NumberOfLeadingZeros > 1 and lIPAddressSplit[iToCount] != 0:
                    dIN()
                else:
                    # This makes it move on
                    CheckingInputLength()

            # This section will check if the Oct is all zeros, but it is currently not being used
            if len(lIPAddressSplit[iToCount]) == NumberOfLeadingZeros:
                dEND()
            # This will see if the Oct is equal to "01" and if so it will move on to dIN()
            if lIPAddressSplit[iToCount] == "01":
                dIN()
            else:
                dEND()
            # Move on to the next Oct
            iToCount += 1


# This section will check if there are four sections in what was split before and then it will make each of those split sections into octets into integers
def CheckingInputLength():
    # This makes the Variable usable in different areas
    global Oct0, Oct1, Oct2, Oct3
    # The program checks if the input is the right length
    if len(lIPAddressSplit)!=4:
        # The script starts over
        dCallingNotAValidIP()
    else:
        # Will see if an error shows up in the code, otherwise it will continue
        try:
            Oct0=int(lIPAddressSplit[0]) #it will be between 1-255
            Oct1=int(lIPAddressSplit[1]) #it will be between 0-255
            Oct2=int(lIPAddressSplit[2]) #it will be between 0-255
            Oct3=int(lIPAddressSplit[3]) #it will be between 0-255

        except Exception:
            dCallingNotAValidIP()

# This check if any of the sections are above 255, this section will assign which class is related to the IP address
def CheckingClassType():
    # The program checks if this is actually a valid IP address
    if all(iIndex in range(0, 256) for iIndex in (Oct0, Oct1, Oct2, Oct3)):
        pass
    else:
        dCallingNotAValidIP()
    # This will print the section in between the text to announce the class
    print('{} is a '.format(sIPAddressInput), end='')
    # This section tests which range the IP address is in
    if Oct0 in range(0, 128):
        print('class A', end='')
    elif Oct0 in range(128, 192):
        print('class B', end='')
    elif Oct0 in range(192, 224):
        print('class C', end='')
    elif Oct0 in range(224, 240):
        print('class D', end='')
    elif Oct0 in range(240, 256):
        print('class E', end='')
    # Fault testing message
    else:
        print("This code is insufficient")
        dCallingNotAValidIP()

# This section will tell the person if it is in any reserved ranges for the IP address, it will also tell you if it a
# braodcast, multicast, network, or unicast address.
def SpecificRanges():
    # This will print the section in between the text to announce the class
    print(' IP address that ', end='')
    # This section will check what "IP type" the input is. Taken from:
    # Short, T. (2023, September). Addressing. Edmonton; NETW1000 - Network Fundamentals.
    if (Oct0 in range(0,1)) or (Oct3 in range(255,256)):
        print('is unassignable', end='')
    elif all(iIndex in range(0,1) for iIndex in (Oct0, Oct1, Oct2, Oct3)):
        print('is reserved identifying a local host or a default route', end='')
    elif Oct0 in range(10,11):
        print('is reserved for private addresses (RFC 1918)', end='')
    elif Oct0 in range(100,101) and Oct1 in range(64, 128):
        print('is reserved for carrier-grade NAT', end='')
    elif Oct0 in range(127,128):
        print('is reserved for local loopback (troubleshooting and identification purposes)', end='')
    elif Oct0 in range(169,170) and Oct1 in range(254,255):
        print('is reserved for link-local address', end='')
    elif Oct0 in range(172,173) and Oct1 in range(17, 32):
        print('is reserved for private addresses', end='')
    elif Oct0 in range(192,193) and all(iIndex in range(0,1) for iIndex in (Oct1, Oct2)):
        print('is reserved by IETF', end='')
    elif Oct0 in range(192,193) and Oct1 in range(0,1) and Oct2 in range(2,3):
        print('is reserved for documentation & examples', end='')
    elif Oct0 in range(198,199) and Oct1 in range(51,52) and Oct2 in range(100,101):
        print('is reserved for documentation & examples', end='')
    elif Oct0 in range(203,204) and Oct1 in range(0,1) and Oct2 in range(113,114):
        print('is reserved for documentation & examples', end='')
    elif Oct0 in range(198,199) and Oct1 in range(19, 20):
        print('is reserved for benchmark testing', end='')
    elif Oct0 in range(192,193) and Oct1 in range(168,169):
        print('is reserved for private addresses', end='')
    # This section tests if it is the broadcast address representing “all hosts” (aka 255.255.255.255)
    elif all(iIndex in range(255,256) for iIndex in (Oct0, Oct1, Oct2, Oct3)):
        print('The broadcast address representing “all hosts”', end='')
    else:
        print('is not reserved', end='')
    # To print the section in between the text
    print(', it is also a ', end='')
    # This section will see if the IP address is a Network, Broadcast, Multicast, or Unicast Address
    if Oct3 in range(0,1):
        print('Network Address', end='')
    elif Oct3 in range(255,256):
        print('Broadcast Address', end='')
    elif Oct0 in range(224, 240):
        print('Multicast Address', end='')
    else:
        print('Unicast Address', end='')

# This section will create the binary section that shows how the IP address would look, it takes away the beginning 0b and add zeros in front of it
def Binary():
    # This section will print the IP address in binary
    BinOct0 = (bin(Oct0).strip('0b')).zfill(8)
    BinOct1 = (bin(Oct1).strip('0b')).zfill(8)
    BinOct2 = (bin(Oct2).strip('0b')).zfill(8)
    BinOct3 = (bin(Oct3).strip('0b')).zfill(8)
    print(' this IP address is {}.{}.{}.{} in Binary'.format(BinOct0, BinOct1, BinOct2, BinOct3), end='')
    # A new line is displayed so that restarting does not look funny
    print(".", end='\n')


    # The script loops because of these
    Input()
    CheckingInputLength()
    CheckingClassType()
    SpecificRanges()
    Binary()

# The program starts
Input()
# It checks the input length
CheckingInputLength()
# It checks what class the IP address is
CheckingClassType()
# It checks what range the IP address is in
SpecificRanges()
# It prints out the IP address in binary
Binary()
