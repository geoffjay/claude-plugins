---
description: Scaffold new Sinatra applications with modern structure, best practices, testing setup, and deployment configuration
---

# Sinatra Scaffold Command

Scaffolds a new Sinatra application with modern project structure, testing framework, and deployment configuration.

## Arguments

- **$1: project-name** (required) - Name of the project/application
- **$2: type** (optional) - Application type: `classic`, `modular`, or `api` (default: `modular`)
- **$3: options** (optional) - JSON string with configuration options:
  - `testing`: `rspec` or `minitest` (default: `rspec`)
  - `database`: `sequel`, `activerecord`, or `none` (default: `sequel`)
  - `frontend`: `none`, `erb`, or `haml` (default: `erb`)

## Usage Examples

```bash
# Basic modular app with defaults
/sinatra-scaffold my-app

# Classic app with RSpec and no database
/sinatra-scaffold simple-app classic '{"testing":"rspec","database":"none","frontend":"erb"}'

# API-only app with Minitest and ActiveRecord
/sinatra-scaffold api-service api '{"testing":"minitest","database":"activerecord","frontend":"none"}'

# Full-featured modular app
/sinatra-scaffold webapp modular '{"testing":"rspec","database":"sequel","frontend":"haml"}'
```

## Workflow

### Step 1: Validate and Initialize

**Actions:**
1. Validate project name format (alphanumeric, hyphens, underscores)
2. Check if directory already exists
3. Parse and validate options JSON
4. Create project directory structure

**Validation:**
```bash
# Check project name
if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo "Error: Invalid project name. Use alphanumeric characters, hyphens, or underscores."
  exit 1
fi

# Check if directory exists
if [ -d "$PROJECT_NAME" ]; then
  echo "Error: Directory '$PROJECT_NAME' already exists."
  exit 1
fi
```

### Step 2: Create Directory Structure

**Classic Structure:**
```
project-name/
├── app.rb
├── config.ru
├── Gemfile
├── Rakefile
├── config/
│   └── environment.rb
├── public/
│   ├── css/
│   ├── js/
│   └── images/
├── views/
│   ├── layout.erb
│   └── index.erb
├── spec/ or test/
└── README.md
```

**Modular Structure:**
```
project-name/
├── app/
│   ├── controllers/
│   │   ├── application_controller.rb
│   │   └── base_controller.rb
│   ├── models/
│   ├── services/
│   └── helpers/
├── config/
│   ├── environment.rb
│   ├── database.yml (if database selected)
│   └── puma.rb
├── config.ru
├── db/
│   └── migrations/
├── lib/
│   └── tasks/
├── public/
│   ├── css/
│   ├── js/
│   └── images/
├── views/
│   ├── layout.erb
│   └── index.erb
├── spec/ or test/
│   ├── spec_helper.rb
│   └── controllers/
├── Gemfile
├── Rakefile
├── .env.example
├── .gitignore
└── README.md
```

**API Structure:**
```
project-name/
├── app/
│   ├── controllers/
│   │   ├── api_controller.rb
│   │   └── base_controller.rb
│   ├── models/
│   ├── services/
│   └── serializers/
├── config/
│   ├── environment.rb
│   ├── database.yml
│   └── puma.rb
├── config.ru
├── db/
│   └── migrations/
├── lib/
├── spec/ or test/
│   ├── spec_helper.rb
│   ├── requests/
│   └── support/
├── Gemfile
├── Rakefile
├── .env.example
├── .gitignore
└── README.md
```

### Step 3: Generate Gemfile

**Base Dependencies (All Types):**
```ruby
source 'https://rubygems.org'

ruby '~> 3.2'

gem 'sinatra', '~> 3.0'
gem 'sinatra-contrib', '~> 3.0'
gem 'puma', '~> 6.0'
gem 'rake', '~> 13.0'
gem 'dotenv', '~> 2.8'

# Add database gems if selected
# gem 'sequel', '~> 5.0' or gem 'activerecord', '~> 7.0'
# gem 'pg', '~> 1.5' # PostgreSQL

# Add frontend gems if not API
# gem 'haml', '~> 6.0' if haml selected

group :development, :test do
  gem 'rspec', '~> 3.12' # or minitest
  gem 'rack-test', '~> 2.0'
  gem 'rerun', '~> 0.14'
end

group :development do
  gem 'pry', '~> 0.14'
end

group :test do
  gem 'simplecov', '~> 0.22', require: false
  gem 'database_cleaner-sequel', '~> 2.0' # if using Sequel
end
```

**Additional Dependencies by Type:**

For modular/API:
```ruby
gem 'rack-cors', '~> 2.0'  # For API
gem 'multi_json', '~> 1.15'
```

For database options:
```ruby
# Sequel
gem 'sequel', '~> 5.0'
gem 'pg', '~> 1.5'

# ActiveRecord
gem 'activerecord', '~> 7.0'
gem 'pg', '~> 1.5'
gem 'sinatra-activerecord', '~> 2.0'
```

### Step 4: Generate Application Files

**Classic App (app.rb):**
```ruby
require 'sinatra'
require 'sinatra/reloader' if development?
require_relative 'config/environment'

get '/' do
  erb :index
end
```

**Modular Base Controller (app/controllers/base_controller.rb):**
```ruby
require 'sinatra/base'
require 'sinatra/json'

class BaseController < Sinatra::Base
  configure do
    set :root, File.expand_path('../..', __dir__)
    set :views, Proc.new { File.join(root, 'views') }
    set :public_folder, Proc.new { File.join(root, 'public') }
    set :show_exceptions, false
    set :raise_errors, false
  end

  configure :development do
    require 'sinatra/reloader'
    register Sinatra::Reloader
  end

  helpers do
    def json_response(data, status = 200)
      halt status, { 'Content-Type' => 'application/json' }, data.to_json
    end
  end

  error do
    error = env['sinatra.error']
    status 500
    json_response({ error: error.message })
  end

  not_found do
    json_response({ error: 'Not found' }, 404)
  end
end
```

**Application Controller (app/controllers/application_controller.rb):**
```ruby
require_relative 'base_controller'

class ApplicationController < BaseController
  get '/' do
    erb :index
  end

  get '/health' do
    json_response({ status: 'ok', timestamp: Time.now.to_i })
  end
end
```

**API Controller (for API type):**
```ruby
require_relative 'base_controller'

class ApiController < BaseController
  before do
    content_type :json
  end

  # CORS for development
  configure :development do
    before do
      headers 'Access-Control-Allow-Origin' => '*'
    end

    options '*' do
      headers 'Access-Control-Allow-Methods' => 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
      headers 'Access-Control-Allow-Headers' => 'Content-Type, Authorization'
      200
    end
  end

  get '/' do
    json_response({
      name: 'API',
      version: '1.0',
      endpoints: [
        { path: '/health', method: 'GET' }
      ]
    })
  end

  get '/health' do
    json_response({ status: 'healthy', timestamp: Time.now.to_i })
  end
end
```

### Step 5: Create Configuration Files

**config.ru:**
```ruby
require_relative 'config/environment'

# Modular
map '/' do
  run ApplicationController
end

# API
# map '/api/v1' do
#   run ApiController
# end
```

**config/environment.rb:**
```ruby
ENV['RACK_ENV'] ||= 'development'

require 'bundler'
Bundler.require(:default, ENV['RACK_ENV'])

# Load environment variables
require 'dotenv'
Dotenv.load(".env.#{ENV['RACK_ENV']}", '.env')

# Database setup (if selected)
# require_relative 'database'

# Load application files
Dir[File.join(__dir__, '../app/**/*.rb')].sort.each { |file| require file }
```

**config/database.yml (if database selected):**
```yaml
default: &default
  adapter: postgresql
  encoding: unicode
  pool: <%= ENV.fetch("DB_POOL", 5) %>
  host: <%= ENV.fetch("DB_HOST", "localhost") %>

development:
  <<: *default
  database: <%= ENV.fetch("PROJECT_NAME") %>_development

test:
  <<: *default
  database: <%= ENV.fetch("PROJECT_NAME") %>_test

production:
  <<: *default
  database: <%= ENV.fetch("DB_NAME") %>
  username: <%= ENV.fetch("DB_USER") %>
  password: <%= ENV.fetch("DB_PASSWORD") %>
```

**config/puma.rb:**
```ruby
workers ENV.fetch('WEB_CONCURRENCY', 2)
threads_count = ENV.fetch('MAX_THREADS', 5)
threads threads_count, threads_count

preload_app!

port ENV.fetch('PORT', 3000)
environment ENV.fetch('RACK_ENV', 'development')

on_worker_boot do
  # Database reconnection if using ActiveRecord
  # ActiveRecord::Base.establish_connection if defined?(ActiveRecord)
end
```

### Step 6: Set Up Testing Framework

**RSpec spec/spec_helper.rb:**
```ruby
ENV['RACK_ENV'] = 'test'

require 'simplecov'
SimpleCov.start

require_relative '../config/environment'
require 'rack/test'
require 'rspec'

# Database cleaner setup (if database)
# require 'database_cleaner/sequel'

RSpec.configure do |config|
  config.include Rack::Test::Methods

  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups

  # Database cleaner (if database)
  # config.before(:suite) do
  #   DatabaseCleaner.strategy = :transaction
  #   DatabaseCleaner.clean_with(:truncation)
  # end
  #
  # config.around(:each) do |example|
  #   DatabaseCleaner.cleaning do
  #     example.run
  #   end
  # end
end
```

**Example spec/controllers/application_controller_spec.rb:**
```ruby
require_relative '../spec_helper'

RSpec.describe ApplicationController do
  def app
    ApplicationController
  end

  describe 'GET /' do
    it 'returns success' do
      get '/'
      expect(last_response).to be_ok
    end
  end

  describe 'GET /health' do
    it 'returns health status' do
      get '/health'
      expect(last_response).to be_ok
      json = JSON.parse(last_response.body)
      expect(json['status']).to eq('ok')
    end
  end
end
```

### Step 7: Create Supporting Files

**.env.example:**
```bash
RACK_ENV=development
PORT=3000

# Database (if selected)
DB_HOST=localhost
DB_NAME=project_name_development
DB_USER=postgres
DB_PASSWORD=

# Session
SESSION_SECRET=your-secret-key-here

# External services
# API_KEY=
```

**.gitignore:**
```
*.gem
*.rbc
/.config
/coverage/
/InstalledFiles
/pkg/
/spec/reports/
/spec/examples.txt
/test/tmp/
/test/version_tmp/
/tmp/

# Environment files
.env
.env.local

# Database
*.sqlite3
*.db

# Logs
*.log

# Editor files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db
```

**Rakefile:**
```ruby
require_relative 'config/environment'

# Database tasks (if using Sequel)
if defined?(Sequel)
  require 'sequel/core'
  namespace :db do
    desc 'Run migrations'
    task :migrate, [:version] do |t, args|
      Sequel.extension :migration
      db = Sequel.connect(ENV['DATABASE_URL'])
      if args[:version]
        puts "Migrating to version #{args[:version]}"
        Sequel::Migrator.run(db, 'db/migrations', target: args[:version].to_i)
      else
        puts 'Migrating to latest'
        Sequel::Migrator.run(db, 'db/migrations')
      end
      puts 'Migration complete'
    end
  end
end

# Testing tasks
require 'rspec/core/rake_task'
RSpec::Core::RakeTask.new(:spec)

task default: :spec
```

**README.md:**
```markdown
# [Project Name]

[Brief description of the project]

## Setup

1. Install dependencies:
   ```bash
   bundle install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Set up database (if applicable):
   ```bash
   rake db:migrate
   ```

## Development

Run the application:
```bash
bundle exec rerun 'rackup -p 3000'
```

Or with Puma:
```bash
bundle exec puma -C config/puma.rb
```

## Testing

Run tests:
```bash
bundle exec rspec
```

## Deployment

[Add deployment instructions]

## API Documentation

[Add API documentation if applicable]
```

### Step 8: Initialize Git Repository

**Actions:**
```bash
cd project-name
git init
git add .
git commit -m "Initial commit: Sinatra application scaffold"
```

### Step 9: Install Dependencies

**Actions:**
```bash
bundle install
```

**Verification:**
- Confirm all gems installed successfully
- Check for any dependency conflicts
- Display next steps to user

## Expected Output

```
Creating Sinatra application: my-app
Type: modular
Options: {"testing":"rspec","database":"sequel","frontend":"erb"}

✓ Created directory structure
✓ Generated Gemfile
✓ Created application files
✓ Set up configuration files
✓ Configured RSpec testing
✓ Created supporting files
✓ Initialized git repository
✓ Installed dependencies

Application created successfully!

Next steps:
  cd my-app
  bundle exec rerun 'rackup -p 3000'

Visit: http://localhost:3000
Tests: bundle exec rspec
```

## Error Handling

- Invalid project name format
- Directory already exists
- Invalid JSON options
- Bundle install failures
- File creation permission errors

## Notes

- All generated code follows Ruby and Sinatra best practices
- Testing framework is fully configured and ready to use
- Development tools (rerun, pry) included for better DX
- Production-ready configuration provided
- Database migrations directory created if database selected
- CORS configured for API applications
