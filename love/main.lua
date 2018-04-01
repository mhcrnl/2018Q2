function love.draw()
	love.graphics.print("SALUT!", 400, 300)
  love.graphics.rectangle("fill",x,200,50,80)
  love.graphics.draw(myImage, 100,100,0,-1,1)
end
function love.update(dt)
  --print(dt)
  x = x + 100 * dt
end

function love.load()
  myImage = love.graphics.newImage("sheep.png")
  
  x=100
end
