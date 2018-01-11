
int stackOpe[255];
int stackOpeTop = -1;
double stackNumber[255];
int stackNumberTop = -1;

int get_pri(int ope)
{
    if (ope == '(')
        return 0;
    if (ope == '+' || ope == '-') 
        return 1;
    if (ope == '*' || ope == '/')
        return 2;
    return -1;
}
void compute(int ope)
{
    double n;
    double n1, n2;

    n1 = stackNumber[stackNumberTop];
    stackNumberTop -= 1;
    n2 = stackNumber[stackNumberTop];
    stackNumberTop -= 1;

    if (ope == '+')
        n = n2 + n1;
    if (ope == '-')
        n = n2 - n1;
    if (ope == '*')
        n = n2 * n1;
    if (ope == '/')
        n = n2 / n1;

    stackNumberTop += 1;
    stackNumber[stackNumberTop] = n;
}

void deal_ope(int ope)
{
    int old_ope;

    if (stackOpeTop < 0 || ope == '(')
    {
        stackOpeTop += 1;
        stackOpe[stackOpeTop] = ope;
        return;
    }

    old_ope = stackOpe[stackOpeTop];

    if (get_pri(ope) > get_pri(old_ope))
    {
        stackOpeTop += 1;
        stackOpe[stackOpeTop] = ope;
        return;
    }

    while (get_pri(ope) <= get_pri(old_ope))
    {
        old_ope = stackOpe[stackOpeTop];
        stackOpeTop -= 1;
        compute(old_ope);
        if (stackOpeTop < 0)
        {
            break;
        }
        old_ope = stackOpe[stackOpeTop];
    }

    stackOpeTop += 1;
    stackOpe[stackOpeTop] = ope;
}

void deal_bracket()
{
    int old_ope = stackOpe[stackOpeTop];

    while (old_ope != '(')
    {
        old_ope = stackOpe[stackOpeTop];
        stackOpeTop -= 1;
        compute(old_ope);
        old_ope = stackOpe[stackOpeTop];
    }
    
    old_ope = stackOpe[stackOpeTop];
    stackOpeTop -= 1;
}
int main()
{
    char string[256] = "113+(26-2)*4/(2+1)";

    int i = 0;
    double value = 0;
    int flag = 0;
    int old_ope;

    while (string[i] != '\0')
    {
        if (string[i] >= '0' && string[i] <= '9')
        {
            value = value * 10 + string[i] - '0';
            flag = 1;
        }
        else 
        {
            if (flag)
            {
                stackNumberTop += 1;
                stackNumber[stackNumberTop] = value;
                flag = 0;
                value = 0;
            }
            if (string[i] == ')')
            {
                deal_bracket();
            }
            else
            {
                deal_ope(string[i]);
            }
        }
        i += 1;
    }

    if (flag)
    {
        stackNumberTop += 1;
        stackNumber[stackNumberTop] = value;
    }

    while (stackOpeTop >= 0)
    {
        old_ope = stackOpe[stackOpeTop];
        stackOpeTop -= 1;
        compute(old_ope);
    }

    value = stackNumber[stackNumberTop];
    stackNumberTop -= 1;
    printf("%s = %lf", string, value);


    return 0;
}
