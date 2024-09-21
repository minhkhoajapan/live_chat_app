const OtherSenderChat = ({msg}) => {
  return (
    <>
      <div className="font-medium mr-2">{msg.sender.username}</div>
        <div className="bg-white rounded-lg p-2 shadow max-w-sm">
          {msg.message && msg.message}
          {msg.file && (
            <img className="max-w-72 min-w-8" src={`http://${baseURL}${msg.file}`} />
          )}
        </div>
    </>
  )
}

export default OtherSenderChat