
def main():
    #minheap = []
    line = "Gene Name: *11111111111111111111111111111111111111111111111111 *Ref_score* [1000, 0, 0]"
    line = line.replace('[', '')
    line = line.replace(']', '')
    line_list = line.split('*')
    gene_name = line_list[1]
    value_factor = line_list[3].split(',')[0]
    #heappush(minheap,[gene_name, value_factor])
    print(gene_name,value_factor)

if __name__ == "__main__": main()