# Extract papers' formula from arxiv

- [x] step1 : Find papers' index.
- [x] step2 : Download papers.
- [x] step3 : Parse papers.
- [x] step4 : Store and clean.
- [ ] step5 : Deploy in my web server. 

# How to use

run in terminal:
```bash
mkdir Downloads
mkdir Outputs
nohup python3 main.py &
```
And the data would be saved in `Outputs` Folder. Check the running status by using:
```bash
tail -f nohup.out
```
and press `Ctrl+c` to quit.
![Run Demo](https://s2.loli.net/2023/01/06/u9skjBZORldao6w.png)
