#include <thread>
#include <iostream>
#include <mutex>
#include <condition_variable>

class Barrier {
	std::mutex mx;
	std::condition_variable cv;
	int ready = 0;
public:
	const int num_threads;
	explicit Barrier(int x) : num_threads(x) {}

	void wait() {
		std::unique_lock<std::mutex> lck(mx);
		ready++;
		if (ready == num_threads) {
			ready = 0;
			cv.notify_all();
		}
		else {
			cv.wait(lck);
		}
	}
};

void output_char(char c, int nt, Barrier* m) {
	while (nt--) {
		std::cout << c;
		m->wait();
	}
}

void synchronized_alphabet() {
	const char* alphabet = "abcdefghijklmnopqrstuvwxyz";
	const int alen = strlen(alphabet);
	std::thread** ts = new std::thread*[alen];
	Barrier b(alen);
	for (int i = 0; i < alen; i++) {
		ts[i] = new std::thread(output_char, alphabet[i], 3, &b);
	}
	for (int i = 0; i < alen; i++) {
		ts[i]->join();
		delete ts[i];
	}
	delete[] ts;
}