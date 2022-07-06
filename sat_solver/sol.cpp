#include <bits/stdc++.h>
using namespace std;
//-----------------------starting time----------------------------
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
//----------------converts number string to integer-------------------
int string_to_integer(string s)
{
    int ans = 0;
    for (auto e : s)
    {
        ans *= 10;
        ans += e - '0';
    }
    return ans;
}
//--------------------taking the basic input from start---------------------
pair<int, int> _input_start() // returns number of literals and clauses
{
    string s;
    vector<string> clauses;
    while (1)
    {
        getline(cin, s);
        if (s[0] == 'c')
        {
            continue;
        }
        else
        {
            break;
        }
    }

    int size_s = s.length();
    
    string literals, num_clauses;
    bool flag = true;
    for (int i = 6; i < size_s; i++)
    {
        if (flag)
        {
            if (s[i] == ' ')
            {
                flag = false;
                continue;
            }
            literals.push_back(s[i]);
        }
        else
        {
            if (s[i] == ' ')
            {
                continue;
            }
            num_clauses.push_back(s[i]);
        }
    }
    pair<int, int> p = {string_to_integer(literals), string_to_integer(num_clauses)};
    return p;
}

//-----------------cnf structure------------------------
struct cnf
{
    vector<vector<int>> clauses;
    vector<int> literal;
};
// ------------pure literal assign----------------------
cnf pure_literal(cnf c)
{
    vector<int> temp(151, -1);
    for (auto e : c.clauses)
    {
        for (auto e1 : e)
        {
            if (temp[abs(e1)] == -1 || temp[abs(e1)] == (e1 > 0))
            {
            }
            else
            {
                temp[abs(e1)] == -2;
            }
        }
    }
    int n = c.literal.size();
    for (int i = 1; i < n; i++)
    {
        if (temp[i] == 0)
        {
            c.literal[i] = 0;
        }
        else if (temp[i] == 1)
        {
            c.literal[i] = 1;
        }
    }
    cnf a;
    for (auto e : c.clauses)
    {
        bool ok = true;
        for (auto e1 : e)
        {
            if (temp[abs(e1)] == -2 || temp[abs(e1)] == -1)
            {
                ok = false;
            }
        }
        if (!ok)
        {
            a.clauses.push_back(e);
        }
    }
    a.literal = c.literal;
    return a;
}

vector<int> sol_literal; // will be used to store the model
//-------------- unit_propogation----------------------
bool ok;
cnf unit_propagation(cnf c)
{

    set<int> s;
    ok = true;

    for (auto e : c.clauses)
    {
        if (e.size() == 1)
        {
            if (s.find(-e[0]) != s.end())
                ok = false;
            else
            {
                s.insert(e[0]);
            }
        }
    }
    if (ok == false)
    {
        return c;
    }
    for (auto e : s)
    {
        c.literal[abs(e)] = (e > 0) ? 1 : 0;
    }
    cnf a;
    for (auto e : c.clauses)
    {
        vector<int> v;
        bool inc = true;
        for (auto e1 : e)
        {
            if (c.literal[abs(e1)] != -1)
            {
                if (((e1 > 0) ? 1 : 0) == (c.literal[abs(e1)]))
                {
                    inc = false;
                    break;
                }
                else
                {
                    continue;
                }
            }
            v.push_back(e1);
        }
        if (inc == true)
        {
            if (!v.size())
            {
                ok = false;
                break;
            }
            else
            {

                a.clauses.push_back(v);
            }
        }
    }
    a.literal = c.literal;
    return a;
}

int choose_literal(cnf c)
{
    cnf a;
    vector<int> v(301, 0);
    for (auto e : c.clauses)
    {
        for (auto e1 : e)
        {
            v[e1 + 150]++;
        }
    }
    int max_val = 0;
    int lit;
    for (int i = 0; i < 301; i++)
    {
        if (v[i] > max_val)
        {
            max_val = v[i];
            lit = i - 150;
        }
    }
    return abs(lit);
}
// chooses the literal which occurs most
int dpll(cnf a)
{
    // unit propogation
    cnf b = unit_propagation(a);
    if (ok == false)
        return 0;
    while (b.clauses.size() != a.clauses.size())
    {
        a = b;
        b = unit_propagation(b);
        if (ok == false)
            return 0;
    }
    b = pure_literal(a);
    while (b.clauses.size() != a.clauses.size())
    {
        a = b;
        b = pure_literal(b);
    }

    if (a.clauses.size() == 0)
    {
        sol_literal = a.literal;
        return 1;
    }
    int d = choose_literal(a);
    b.clauses.push_back({d});
    if (dpll(b))
    {
        return 1;
    }

    a.clauses.push_back({-d});

    if (dpll(a))
    {
        return 1;
    }
    return 0;
}
int main()
{
    // for input-output from files
    freopen("input.cnf", "r", stdin);
    freopen("output.txt", "w", stdout);

    // for basic input in stating of cnf
    pair<int, int> p = _input_start();
    cnf c; // cnf file
    //literals are -1 if no value is assigned ,1 if they are true ,0 if they are false. 
    for (int i = 0; i < p.first + 1; i++)
    {
        c.literal.push_back(-1);  
    }

    for (int i = 0; i < p.second; i++)
    {
        int q;
        vector<int> v;
        cin >> q;
        while (q != 0)
        {
            v.push_back(q);
            cin >> q;
        }
        c.clauses.push_back(v);
    }

    int ok = dpll(c);
    if (ok == 0)
    {
        cout << "Cnf is unsatisfiable"
             << "\n";
    }
    else
    {
        cout << "Answer Exist!  Model is --> "
             << "\n";
        int i;
        for (i = 1; i < p.first+1; i++)
        {
            if (sol_literal[i] == -1)
            {
                cout << i << " ";
            }
            else if (sol_literal[i] == 1)
            {
                cout << i << " ";
            }
            else
            {
                cout << -i << " ";
            }
        }
    }
    cout << endl;
    cout << "Time:" << 1000 * ((double)clock()) / (double)CLOCKS_PER_SEC << " milliseconds\n";
}
