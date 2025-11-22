#include<stdio.h>
#include<stdlib.h>
struct node {
    char d;
    int f;
    struct node *l, *r;
};

struct node* Create( char data, int freq ) {
    struct node* newNode = (struct node*)malloc(sizeof(struct node));
    newNode->d = data;
    newNode->f = freq;
    newNode->l = newNode->r = NULL;
    return newNode;
}

struct node* HuffmanTree(char data[], int freq[], int size)
{
    struct node** nodes = (struct node**)malloc(size*sizeof(struct node*));
    for(int i = 0; i<size; i++)
    {
        nodes[i] = Create(data[i], freq[i]);
    }
    while(size>1)
    {
        for(int i = 0; i<size-1; i++)
        {
            for(int j = 0; j<size-i-1;j++)
            {
                if(nodes[j]->f>nodes[j+1]->f)
                {
                    struct node* temp = nodes[j];
                    nodes[j] = nodes[j+1];
                    nodes[j+1] = temp;
                }
            }
        }
        struct node *new = Create('$', nodes[0]->f + nodes[1]->f);
        new->r = nodes[1];
        new->l = nodes[0];
        nodes[0] = new;
        for(int i = 1; i<size-1; i++)
        {
            nodes[i] = nodes[i+1];
        }
        size--;
    }
    struct node* root = nodes[0];
    free(nodes);
    return root;
}
void printCode(struct node* root, char data[],int h)
{
    if(root==NULL)
    {
        return;
    }
    if(root->d!='$')
    {
        data[h] = '\0';
        printf("%c : %s\n", root->d, data);
    }
    data[h] = '0';
    printCode(root->l, data, h+1);
    data[h] = '1';
    printCode(root->r,data, h+1);
}

int main()
{
    char data[] = {'a','b', 'c'};
    int freq[] = {12,43,11};
    struct node* root = HuffmanTree(data,freq,3);
    char notanki[100];
    printCode(root,notanki ,0);

}