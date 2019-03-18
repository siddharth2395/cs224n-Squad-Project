from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        context = request.form['context']
        question = request.form['question']
        data = '{"data": [{"title": "","paragraphs": [{"context": "' + context + '","qas": [{"question": "' + question + '","id": "0"}]}]}]}'
        with open('data/test_input.json', 'w') as f:
            f.write(data)
        f.close()
        import subprocess, sys
        ## command to run - tcp only ##
        cmd = "python code/main.py --experiment_name=bidaf_best --dropout=0.15 --batch_size=60 --hidden_size_encoder=150 --embedding_size=100 --do_char_embed=False --add_highway_layer=True --rnet_attention=False --bidaf_attention=True --answer_pointer_RNET=False --smart_span=True --hidden_size_modeling=150 --mode=official_eval --json_in_path=data/test_input.json --json_out_path=predictions_bidaf.json --ckpt_load_dir=experiments/bidaf_best/best_checkpoint"
        ## run it ##
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        ## But do not wait till netstat finish, start displaying output immediately ##
        while True:
            out = p.stderr.read(1)
            if out == '' and p.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()
        out = None
        with open('predictions_bidaf.json', 'r') as f:
            out = f.readlines()
        f.close()
        print out
        import json
        x = json.loads(out[0])
        print x['0']
        return render_template('index.html', c=context, q=question, ans=x['0'])

    else:

        return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0')
