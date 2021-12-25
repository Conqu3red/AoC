#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <variant>
#include <stdint.h>
#include <set>
#include <map>
#include <unordered_map>
#include <tuple>
#include <cmath>
#include "robin_hood.h"

using namespace std;

inline void hash_combine(std::size_t& seed) { }

template <typename T, typename... Rest>
inline void hash_combine(std::size_t& seed, const T& v, Rest... rest) {
    std::hash<T> hasher;
    seed ^= hasher(v) + 0x9e3779b9 + (seed<<6) + (seed>>2);
    hash_combine(seed, rest...);
}

#define MAKE_HASHABLE(type, ...) \
    namespace std {\
        template<> struct hash<type> {\
            std::size_t operator()(const type &t) const {\
                std::size_t ret = 0;\
                hash_combine(ret, __VA_ARGS__);\
                return ret;\
            }\
        };\
    }

struct Instruction {
    string name;
    string op1;
    string op2s;
    int64_t op2i;
};


// for string delimiter
vector<string> split(string s, string delimiter) {
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    string token;
    vector<string> res;

    while ((pos_end = s.find (delimiter, pos_start)) != string::npos) {
        token = s.substr (pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back (token);
    }

    res.push_back (s.substr (pos_start));
    return res;
}

vector<Instruction> load_data() {
    vector<Instruction> instructions;
    string delimiter = " ";
    ifstream file("input.txt");
    string line;

    while (getline(file, line)) {
        auto tokens = split(line, delimiter);
        string op2;
        int64_t op2i = 0;
        if (tokens.size() > 2) {
            op2 = tokens[2];
            if (tokens[2] != "w" && tokens[2] != "x" && tokens[2] != "y" && tokens[2] != "z") {
                op2i = stoll(tokens[2]);
                op2 = "";
            }
        }
        instructions.push_back(Instruction {tokens[0], tokens[1], op2, op2i});
    }

    file.close();
    return instructions;
}

struct Registers {
    int64_t w = 0, x = 0, y = 0, z = 0;
    bool operator ==(const Registers &other) const {
        return w == other.w && x == other.x && y == other.y && z == other.z;
    }

    int64_t &get(std::string name) {
        if (name == "w") return w;
        if (name == "x") return x;
        if (name == "y") return y;
        if (name == "z") return z;
        
        return w;
    }
};
MAKE_HASHABLE(Registers, t.w, t.x, t.y, t.z)

class BruteForce {
public:
    vector<Instruction> instructions;
    robin_hood::unordered_flat_map<Registers, int64_t> states;
    robin_hood::unordered_flat_map<Registers, int64_t> new_states;
    int64_t smallest = 0x7FFFFFFFFFFFFFFF;

    BruteForce(vector<Instruction> instructions) {
        this->instructions = instructions;
    }

    void run() {
        vector<int64_t> input_indexes = {0};
        for (int64_t index = 0; index < instructions.size(); index++) {
            auto &i = instructions[index];
            if (i.name == "inp") input_indexes.push_back(index + 1);
        }
        states.insert({Registers {0, 0, 0, 0}, 0});
        for (int i = 0; i < 14; i++) {
            new_states = robin_hood::unordered_flat_map<Registers, int64_t>();

            for (auto [r, s] : states) {
                get_all_states(r, input_indexes[i], s, i + 1);
            }
            // BUG: one bit is missing

            states = new_states;

            cout << "Bit " << i + 1 << " States: " << states.size() << "\n";
        }
        
        for (auto [r, s] : states) {
            get_all_states(r, input_indexes[14], s, 15);
        }
        cout << "Smallest: " << smallest << "\n";
    }

    void get_all_states(Registers r, int64_t index, int64_t n, int64_t bits_done) {
        auto g2 = [&r](Instruction i){ return i.op2s.empty() ? i.op2i : r.get(i.op2s); };

        for (int64_t ind = index; ind < instructions.size(); ind++) {
            auto &i = instructions[ind];

            if (i.name == "inp") {
                for (int64_t b = 1; b < 10; b++) {
                    r.get(i.op1) = b;
                    auto nn = n + (b * ((int64_t)std::pow(10, 14 - bits_done)));
                    //cout << r.w << " " << r.x << " " << r.y << " " << r.z << "\n";
                    
                    // discard if it's higher
                    if (new_states.find(r) != new_states.end() && new_states[r] <= nn) continue;

                    new_states[r] = nn;
                }
                return;
            }
            else if (i.name == "add") r.get(i.op1) = r.get(i.op1) + g2(i);
            else if (i.name == "mul") r.get(i.op1) = r.get(i.op1) * g2(i);
            else if (i.name == "div") r.get(i.op1) = r.get(i.op1) / g2(i);
            else if (i.name == "mod") r.get(i.op1) = r.get(i.op1) % g2(i);
            else if (i.name == "eql") r.get(i.op1) = (int64_t)(r.get(i.op1) == g2(i));
        }

        if (r.z == 0) {
            if (n < smallest) {
                smallest = n;
                cout << "new smallest: " << n << "\n";
            }
        }
    }
};

int main() {
    auto instructions = load_data();
    BruteForce b(instructions);
    b.run();
    return 0;
}