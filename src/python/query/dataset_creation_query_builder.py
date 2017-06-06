from structure.bq_proj_structure import *


##### Functions to build queries against public GitHub data to extract data on specific repos


# Convert a file containing a list of repo names into a comma separated, double quoted list for SQL queries
def comma_separated_quoted_repo_names(file):
    with open(file, encoding = 'utf-8') as f:
        lines = f.readlines()
    return ','.join(['"%s"' % line.strip() for line in lines])
    
    
# Commits
# repos is a comma separated, double quoted list of repo names
def build_query_commits(repos):
    return """
    SELECT
      repo_name,
      commit,
      tree,
      parent,
      subject,
      message,
      author.date,
      committer.date,
      encoding
    FROM
      FLATTEN([%s:%s.%s], repo_name)
    WHERE
      repo_name IN ( %s )

    """ % (project_bq_public_data, dataset_github_repos, table_github_repos_commits, comma_separated_quoted_repo_names(repos))
    
    
# Files
# repos is a comma separated, double quoted list of repo names
def build_query_files(repos):
    return """
    SELECT
      *
    FROM
      [%s:%s.%s]
    WHERE
      repo_name IN ( %s )
    """  % (project_bq_public_data, dataset_github_repos, table_github_repos_files, comma_separated_quoted_repo_names(repos))


# Contents
# repos is a comma separated, double quoted list of repo names
def build_query_contents(repos):
    return """
        SELECT
      *
    FROM (
      SELECT
        *
      FROM (
        SELECT
          *
        FROM (
          SELECT
            *
          FROM
            [%s:%s.%s]
          WHERE
            repo_name IN ( %s )))) AS files
    LEFT JOIN (
      SELECT
        *
      FROM (
        SELECT
          *
        FROM (
          SELECT
            *
          FROM
            [%s:%s.%s]
          WHERE
            id IN (
            SELECT
              id
            FROM
              [%s:%s.%s]
            WHERE
              repo_name IN ( %s ) )))) AS contents
    ON
      files.id=contents.id

    """ % (project_bq_public_data, dataset_github_repos, table_github_repos_files, comma_separated_quoted_repo_names(repos),
           project_bq_public_data, dataset_github_repos, table_github_repos_contents,
           project_bq_public_data, dataset_github_repos, table_github_repos_files, comma_separated_quoted_repo_names(repos))
    
    
# GitHub Archive activity
# repos is a comma separated, double quoted list of repo names
# year is a string
def build_query_gh_archive(repos, year):
    return """
    SELECT
      *
    FROM
      [%s:%s.%s]
    WHERE
      repo.name IN ( %s )
    """ % (project_github_archive, dataset_gh_archive_year, year, comma_separated_quoted_repo_names(repos))
    

# Combine years of GitHub archive
def build_query_combine_years_gh_archive(dataset, years):
    tables = ['[%s:%s.%s]' % (project_bioinf, dataset, table_archive(year)) for year in years]
    return 'SELECT * FROM ( SELECT * FROM %s )' % '), (SELECT * FROM '.join(tables)
    
    
# Languages used in each repo
# repos is a comma separated, double quoted list of repo names
def build_query_languages(repos):
    return """
    SELECT
      *
    FROM
      [%s:%s.%s]
    WHERE
      repo_name IN ( %s )
    """ % (project_bq_public_data, dataset_github_repos, table_github_repos_languages, comma_separated_quoted_repo_names(repos))
    
    
# License for each repo
# repos is a comma separated, double quoted list of repo names
def build_query_licenses(repos):
    return """
    SELECT
      *
    FROM
      [%s:%s.%s]
    WHERE
      repo_name IN ( %s )
    """ % (project_bq_public_data, dataset_github_repos, table_github_repos_licenses, comma_separated_quoted_repo_names(repos))
    
    
    
    
    
    
    
    
    
    
    
    
    
    