#include <stdio.h>

int getPass (char* b) {
	if (b[0] == 'c') {
	if (b[1] == 'a') {
	if (b[2] == 'n') {
	if (b[3] == '_') {
	if (b[4] == 'd') {
	if (b[5] == 'i') {
	if (b[6] == 'g') {
	if (b[7] == '_') {
	if (b[8] == 'i') {
	if (b[9] == 't') {
	if (b[10] == '?') {
		return (1);
	}}}}}}}}}}}

	return (0);
}

int main (int argc, char* argv) {
	char buffer[64];

	printf("Welcome to whatchamacallit\n");
	printf("What is the password? ");

	scanf("%65s", buffer);

	if (getPass (buffer)) {
		printf ("Password is correct!\n");
		return (0);
	}
	printf ("Password is incorrect.\n");
	return (0);
}
