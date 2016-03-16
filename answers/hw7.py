import sys


class AddressResolver:
    def __init__(self, mem_file):
        self.mem_pages = []
        self.disk_pages = []

        infile = open(mem_file)
        if not infile:
            print("File not found")
            exit(0)

        infile.readline()
        base_addr = int(infile.readline().split()[2][2:], 16)
        self.base_page_index = base_addr // 32

        for iter in range(0, 2):
            while True:
                line = infile.readline()
                if line.strip() == '~~~':
                    break

            for page in range(0, 128):
                page_content = []
                content = infile.readline().split()[2:]
                for item in content:
                    page_content.append(int(item, 16))
                if iter == 0:
                    self.mem_pages.append(page_content)
                else:
                    self.disk_pages.append(page_content)
            infile.readline()

    def print_mem(self):
        print("Memory Content:")
        counter = 0
        for page_content in self.mem_pages:
            print("page %0.2X" % counter),
            for item in page_content:
                print(" %0.2X" % item),
            print("")
            counter += 1
        print("Disk Content:")
        counter = 0
        for page_content in self.disk_pages:
            print("page %0.2X" % counter),
            for item in page_content:
                print(" %0.2X" % item),
            print("")
            counter += 1

    def resolve(self, address):

        binary = format(int(address, 16), 'b').zfill(16)
        pde_index = binary[3:6]
        pte_index = binary[6:11]
        offset = binary[11:16]
        print("Virtual Address " + address + "(" + pde_index + " " + pte_index + " " + offset + ")")

        pde_value = self.mem_pages[self.base_page_index][int(pde_index, 2)]
        pde_valid = pde_value // 128
        pde_entry = pde_value - pde_valid * 128
        print("  --> pde_index:" + hex(int(pde_index, 2)) + "(00" + pde_index + ")"),
        print("  pde contents:(" + hex(pde_value) + ", " + bin(pde_value)[2:].zfill(8) + ", valid " +
              str(pde_valid) + ", pfn " + hex(pde_entry) + ")")

        pte_value = self.mem_pages[pde_entry][int(pte_index, 2)]
        pte_valid = pte_value // 128
        pte_entry = pte_value - pte_valid * 128
        print("    --> pte_index:" + hex(int(pte_index, 2)) + "(" + pte_index + ")"),
        print("  pte contents:(" + hex(pte_value) + ", " + bin(pte_value)[2:].zfill(8) + ", valid " +
              str(pte_valid) + ", pfn " + hex(pte_entry) + ")")
        if pte_valid == 0 and pte_entry == 127:
            print("      --> Memory location do not exist")
        phy_addr = pte_entry * 32 + int(offset, 2)
        if pte_valid == 1:
            print("      --> To Physical Address " + hex(phy_addr) + "(" + bin(phy_addr)[2:].zfill(13) + ")"),
            print("  --> Value: " + hex(self.mem_pages[pte_entry][int(offset, 2)]))
        else:
            print("      --> To Disk Sector Address " + hex(phy_addr) + "(" + bin(phy_addr)[2:].zfill(13) + ")"),
            print("  --> Value: " + hex(self.disk_pages[pte_entry][int(offset, 2)]))

if __name__ == '__main__':
    resolver = AddressResolver("../all/04-1-spoc-memdiskdata.md")
    resolve_list = ["6653", "1c13", "6890", "0af6", "1e6f"]
    sys.stdout = open("hw7_answer.txt", 'w')
    for item in resolve_list:
        resolver.resolve(item)
        print("")