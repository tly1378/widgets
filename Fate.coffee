command: "python3 ./tool.py"
refreshFrequency: 60000

render: (output) ->
  """
  <div style="
    width: 304px;
    height: 304px;
    padding: 20px;
    margin: 14px;
    background-color: rgba(0,0,0,0.8);
    color: white;
    border-radius: 16px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    font-family: Helvetica, Arial, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  ">
    #{output}
  </div>
  """

